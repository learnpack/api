import serpy
from django.contrib.auth.models import User, Group
from .models import CredentialsGithub
from django.db import models
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from learnpack.email import send_email_message

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
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print(username, "username", password, "Password" )
        if username and password:
            user = authenticate(request=self.context.get('request'),username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code=403)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code=403)

        attrs['user'] = user
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
    def validate(self, data):
        if User.objects.filter(email= data["email"]).first() is not None:
            raise serializers.ValidationError("That email is already in use.")
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
        
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        send_email_message("email_validation_link", user.email, data={"link": f"/v1/auth/email/validate/{token}", "subject": "Validate Email"})
        return user
        
    def update(self, validated_data):
        _user = self.context['request'].user
        user = super(RegistrationSerializer, self).update(_user, validated_data)
        if _user.email != user.email:
            user.is_active = False
            user.save()
            Token.objects.filter(user__id=user.id).delete()
            token, created = Token.objects.get_or_create(user=user)
            send_email_message("email_validation_link", user.email, data={"link": f"/v1/auth/email/validate/{token}"})
        
        
