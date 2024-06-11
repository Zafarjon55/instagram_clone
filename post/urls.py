from django.urls import path
from . import views

urlpatterns = [
    path('posts/',views.Postviewlist.as_view())
]
