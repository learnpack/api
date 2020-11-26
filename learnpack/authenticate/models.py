from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db import models
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
import rest_framework.authtoken.models
from django.utils import timezone


class CredentialsGithub(models.Model):
    github_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    
    token = models.CharField(max_length=255)
    email = models.CharField(blank=False, unique=True, max_length=150)
    avatar_url = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    blog = models.CharField(max_length=150)
    bio = models.CharField(max_length=255)
    company = models.CharField(max_length=150)
    twitter_username = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class CredentialsQuickBooks(models.Model):
    quibooks_code = models.CharField(max_length=255, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    quibooks_realmid = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class Token(rest_framework.authtoken.models.Token):
    '''
    create multi token per user - override default rest_framework Token class
    replace model one-to-one relationship with foreign key
    '''
    key = models.CharField(max_length=40, db_index=True, unique=True)
    #Foreign key relationship to user for many-to-one relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    token_type = models.CharField(max_length=64, default='temporal')
    expires_at = models.DateTimeField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        # by default token expires one day after
        if self.expires_at == None:
            utc_now = timezone.now()
            if self.token_type == 'login':
                self.expires_at = utc_now + timezone.timedelta(days=1)
            else:
                self.expires_at = utc_now + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def create_temp(user):
        token, created = Token.objects.get_or_create(user=user, token_type= "temporal")
        return token

    def get_or_create(user):
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            now = timezone.now()
            if token.expires_at < now:
                token.delete()
                token = Token.objects.create(user=user)

        return token
    
    def get_valid(token, token_type="temporal"):
        utc_now = timezone.now()
        _token = Token.objects.filter(key=token, expires_at__gt=utc_now, token_type=token_type).first()
        return _token


    class Meta:
        # ensure user and name are unique
        unique_together = (('user', 'token_type'),)