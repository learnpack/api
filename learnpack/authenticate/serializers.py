import serpy
from django.contrib.auth.models import User, Group
from .models import CredentialsGithub
from django.db import models
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Token
from learnpack.utils import ValidationException
from learnpack.email import send_email_message
from django.contrib.auth.hashers import make_password

class GithubSmallSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    avatar_url = serpy.Field()
    name = serpy.Field()

# Create your models here.
class UserSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    id = serpy.Field()
    email = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    github = serpy.MethodField()

    def get_github(self, obj):
        github = CredentialsGithub.objects.filter(user=obj.id).first()
        if github is None:
            return None
        return GithubSmallSerializer(github).data


class GroupSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    id = serpy.Field()
    name = serpy.Field()


class AuthSerializer(serializers.Serializer):
    identification = serializers.CharField(label="Username or email address")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        identification = attrs.get('identification')
        password = attrs.get('password')
        if identification and password:
            if "@" in identification:
                email = identification
                _user = User.objects.filter(email= email).first() 
                if _user is None:
                    raise ValidationException("User with that email and password not found")
                user = authenticate(request=self.context.get('request'),username=_user.username, password=password)
                print(user)
            else:
                username = identification
                user = authenticate(request=self.context.get('request'),username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code=403)
        else:
            msg = 'Must include "username/email" and "password".'
            raise serializers.ValidationError(msg, code=403)
        attrs['user'] = user
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def validate(self, data):
        print("VALIDATE CALLED")
        user = self.context['request'].user
        print(user)
        if user.is_anonymous:
            if User.objects.filter(email= data["email"]).first() is not None:
                raise serializers.ValidationError("That email is already in use.")
        print (data)
        return data

    def create(self, validated_data):
        print("CALLING CREATE METHOD")
        user = User(
            username= self.validated_data["username"],
            email= self.validated_data["email"],
            password= self.validated_data["password"]
        )
        if "first_name" in validated_data:
            user.first_name = validated_data["first_name"]    
        
        if "last_name" in validated_data:
            user.first_name = validated_data["last_name"]    
        user.set_password(user.password)
        user.is_active = False
        user.save()
        print("USER IS ACTIVE: ", user.is_active)
        token, created = Token.objects.get_or_create(user=user, token_type="login")
        send_email_message("email_validation_link", user.email, data={"link": f"/v1/auth/email/validate/{token}", "subject": "Validate Email"})
        return user
        
    def update(self, user ,validated_data):
        _user = user
        old_password =  _user.password
        old_email = _user.email
        if _user.check_password(validated_data.get('password')):
            validated_data.pop('password')
            user = super(RegistrationSerializer, self).update(_user, validated_data)
        else:
            Token.objects.filter(user__id=user.id).delete()
            token, created = Token.objects.get_or_create(user=user, token_type="temporal")
            send_email_message("password_reset_link", user.email, data={"link": "/v1/auth/changepassword/", "subject":"Password reset link"})
        if old_email != user.email:
            user.is_active = False
            Token.objects.filter(user__id=user.id).delete()
            token, created = Token.objects.get_or_create(user=user, token_type="temporal")
            send_email_message("email_validation_link", user.email, data={"link": f"/v1/auth/email/validate/{token}"})
        user.save()
        return user
        
