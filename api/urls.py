
# from django.contrib import admin
# from rest_framework.authtoken import views
from django.urls import path
# from .views import ()
import rest_framework.authentication

from api.views import LikeView, LoginView, PostView, RegisterView




app_name = 'api'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('like/<int:post_id', LikeView.as_view(), name='like_id'),
    path('like', LikeView.as_view(), name='like'),
    path('post', PostView.as_view(), name='post'),
    path('post/<int:post_id>', PostView.as_view(), name='post_id'),

    ]





