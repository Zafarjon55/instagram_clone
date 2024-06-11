from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny
from .models import Post
from shared.pagination import CustomPagination
# Create your views here.

class Postviewlist(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]
    pagination_class =  CustomPagination

    def get_queryset(self):
        return Post.objects.all()
