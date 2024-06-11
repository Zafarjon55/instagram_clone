from rest_framework import serializers
from .models import User, UserConfirmation, VIA_EMAIL, VIA_PHONE,NEW,CODE_VERIFIED,DONE,PHOTO_DONE
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from shared.utils import check_email_or_phone, send_email, send_phone,check_user_type
from rest_framework.exceptions import ValidationError,PermissionDenied
from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserSerializers, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] =  serializers.CharField(required=False)
       

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status'
        )

        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False},
            # 'access':{'access': User.token()['access']},
            # 'refresh':{User.token()['refresh_token']},
        }

    def create(self, validation_data):
        user = super(UserSerializers, self).create(validation_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone(user.phone_number, code)

        user.save()
        return user

    def validate(self, data):
        super(UserSerializers, self).validate(data)
        data = self.auth_validate(data)

        return data
    @staticmethod
    def auth_validate(data):
        user_input = str(data.get("email_phone_number")).lower()

        input_type = check_email_or_phone(user_input)

        if input_type == "email":
            data = {
                'email':user_input,
                'auth_type':VIA_EMAIL
            }
        elif input_type == "phone":
            data = {
                'phone':user_input,
                'auth_type':VIA_PHONE
            }
        else:
            data = {
                'status':False,
                'message':"Email yoki telefon xato shekilli"
            }
            raise ValidationError(data)
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tokens'] = instance.token()
        return representation







class UserChangeSerializer(serializers.Serializer):
    first_name=serializers.CharField(max_length=255,write_only=True,required=True)
    last_name=serializers.CharField(max_length=255,write_only=True,required=True)
    username=serializers.CharField(write_only=True,required=True)
    password=serializers.CharField(write_only=True,required=True)
    confirm_password=serializers.CharField(write_only=True,required=True)
    
    def validate(self,data):
        password=data.get('password')
        confirm_password=data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(
                {
                    'message':'Parol mos kelmayapti !!!'
                }
            )
            
        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data
    
    
    def validate_first_name(self,first_name):
        if len(first_name) < 3 or len(first_name) >30:
            data = {
                "message":"Ism 3 dan kop va 30 tadan kam belgi bolishi kerak! "
            }
            raise ValidationError(data)

        if first_name.isdigit():
            data = {
                "message":"isim faqat raqamlardan iborat bolshi mumkin emas! "
            }
            raise ValidationError(data)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.password = validated_data.get('password',instance.password)
        
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_type == CODE_VERIFIED:
            instance.auth_type=DONE            
        instance.save()
        
        return instance

class LoginSerializers(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__((self,LoginSerializers).__init__(*args,**kwargs))
        self.fields['userinput'] = serializers.CharField(required = True)
        self.fields['username'] = serializers.CharField(required = True,read_only = True)
        
        
    def auth_validate(self,data):
        user_input = data.get('user_input')

        try:
            if check_user_type(user_input) == 'username':
                username = user_input
            elif check_user_type(user_input) == 'email':
                user = self.get_user(email__iexact=user_input)
                username = user.username
            elif check_user_type(user_input) == 'phone':
                user = self.get__user(phone_number=user_input)
                username = user.username
                
            else:
                
                raise ValidationError({
                    "message":" Siz xato login malumotlarini kiritdingiz! "
                })
                
            authentication_kwargs ={
                self.username_field: username,
                'password': data['password']
            }
        
        except Exception:
            print()
        hozirgi_user = User.objects.filter(username__iexact=username).first()

        if hozirgi_user is not None and hozirgi_user.auth_status in [NEW,CODE_VERIFIED]:
            raise ValidationError({
                "message":"Siz to'liq ro'yxatdan o'tdingiz ! "
            })
        
        user =authenticate(**authentication_kwargs)
        
        if user is not None:
            self.user
        else:
            raise ValidationError({
                "message":"Siz login qilaolmaysiz ! "
            })
            
        def validate(self,data):
            self.auth_validate(data)
            print('auth_validate')
            if self.user.auth_status not in [DONE,PHOTO_DONE]:
                raise PermissionDenied("Siz login qila olmaysiz !!!")
            print("validate")
            data = self.user.token()
            data['auth_status']=self.user.auth_status
            data['name']=self.user.first_name

            return data

        def get_user(self,**kwargs):
            user = User.objects.filter(**kwargs)
            if not user.exists():
                raise ValidationError({
                    "message":"Xatolik"
                })
            
            return user.first()
        
            
class ChangeUserPhotoSerializers(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    
    def update(self,instance,validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = photo
            instance.auth_status = PHOTO_DONE
            instance.save()
            
        return instance