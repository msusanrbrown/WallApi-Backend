

from django.contrib.auth.models import User
from .models import Like, Post
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db.models import Q
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import serpy
from rest_framework import status
from .exceptions import ValidationException



class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(label='Password',
                                     style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            email = email.lower()
            user = User.objects.filter(Q(email__iexact=email) | Q(username=email)).first()
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationException(msg, code=403)
            if user.check_password(password) != True:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationException(msg, code=403)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
        else:
            msg = 'Must include "username" and "password".'
            raise ValidationException(msg, code=403)

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationException("Password fields didn't match.", status.HTTP_400_BAD_REQUEST)

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        exclude = ()

class GetUserSerializer(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()

class GetPostSerializer(serpy.Serializer):
    id = serpy.Field()
    description = serpy.Field()
    created_at = serpy.Field()
    updated_at = serpy.Field()
    user = GetUserSerializer()


        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        exclude = ()
        
class GetLikeSerializer(serpy.Serializer):
    id = serpy.Field()
    user = GetUserSerializer()
    status = serpy.Field()
    
    