from django.db import models
from shared.models import BaseModel
from user.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='images/post_images',validators=[FileExtensionValidator])
    post = models.TextField()

    class Meta:
        db_table = 'post'


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    comment = models.CharField(max_length=255)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comemment')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='commentComment'
    )

    class Meta:
        db_table = 'comment'


class CommentLike(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='commentlikes')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='commentlike')

    class Meta:
        db_table = 'comment_like'


class Like(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        db_table = 'like'
