from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import GetLikeSerializer, GetPostSerializer, LikeSerializer, PostSerializer, RegisterSerializer, AuthSerializer
from rest_framework import generics
from .permissions import IsGetOrIsAuthenticated
from rest_framework import status
from .models import Post, Like
from rest_framework.exceptions import NotFound, ValidationError


class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):

        serializer = AuthSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.get_or_create(user=user, token_type='login')
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})


class PostView(APIView):
    permission_classes = (IsGetOrIsAuthenticated,)            

    def get(self, post_id = None):
        if post_id:
            items = Post.objects.filter(is_deleted=False, id = post_id).first()
            if not items:
                raise NotFound('Post does not exist')
            serializer = PostSerializer(items)
            return Response(serializer.data)


        items = Post.objects.filter(is_deleted=False)
        
        serializer = GetPostSerializer(items, many=True)
        return Response(serializer.data)


    def post(self, request):
        many = isinstance(request.data, list)
        serializer = PostSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)            

    def get(self, request, post_id):

        items = Like.objects.filter(post__id=post_id)
        
        users = GetLikeSerializer(items, many=True)
        return Response(users.data)


    def post(self, request):
        user_id = request.POST.get('user')
        post_id = request.POST.get('post')
        
        if not user_id or not post_id:
            raise ValidationError('post or user is needed')
        
        item = Like.objects.filter(user__id = user_id, post__id = post_id).first()
        
        if not item:
            serializer = LikeSerializer(data=request.data)
        else:
            serializer = LikeSerializer(item, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


