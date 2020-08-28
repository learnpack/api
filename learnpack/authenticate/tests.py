from test.support import EnvironmentVarGuard # Python >=3
from django.test import TestCase, override_settings
from django.apps import apps
from django.conf import settings
import os
from django.urls.base import reverse_lazy, reverse
from mixer.backend.django import mixer
from rest_framework.test import force_authenticate, APIClient
from django.contrib.auth.models import User, Group
from learnpack.authenticate.models import CredentialsGithub, Token
# Create your tests here.

@override_settings(EMAIL_NOTIFICATIONS_ENABLED=False)
class AuthenticateTestSuite(TestCase):
    """
    Endpoint tests for Invites
    """
    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.user.set_password('pass1234')
        self.token, created = Token.objects.get_or_create(user=self.user, token_type="login")
        self.user.save()

        self.env = EnvironmentVarGuard()
        self.env.set('ENABLE_NOTIFICATIONS', 'FALSE')

        self.client = APIClient()
        params = { "user": self.user }
        github = mixer.blend('authenticate.CredentialsGithub', **params)
        github.save()

    def test_get_users(self):
        url = reverse_lazy('authenticate:user')
        response = self.client.get(url)
        users = response.json()
        
        # total_users = User.objects.all().count()
        self.assertEqual(1,len(users),"The total users should match the database")


    def test_get_me(self):
        url = reverse_lazy('authenticate:user_me')
        response = self.client.get(url)
        users = response.json()
        
        # total_users = User.objects.all().count()
        self.assertEqual(1,len(users),"I should be able to request my own information using user/me")

    def test_duplicate_email_or_username(self):
        url = reverse_lazy('authenticate:sign_up')
        print(url)
        response = self.client.post(url, data={"username":self.user.username, "password":"pass1234", "email": self.user.email})
        response_json = response.json()
        print(response_json)
        self.assertEquals(response.status_code, 400, "Same email/username should trigger error")

    def test_put_username(self):
        url = reverse('authenticate:user_me')
        print(url)
        print("AUTHENTICATED: ", self.user.is_authenticated)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data={"username":"bob", "password":"pass1234", "email": self.user.email})
        response_json = response.json()
        print(response_json, "RESPONSE")
        print("STATUS: ", response.status_code)
        self.assertEquals(response.status_code, 200, "Post request with change to username should not trigger error")

    def test_put_password(self):
        url = reverse_lazy('authenticate:user_me')
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data={"username":self.user.username, "password":"pass234", "email": self.user.email})
        response_json = response.json()
        print(response_json)
        self.assertEquals(response.status_code, 200, "Post request with change to password should not trigger error")
            

    def test_put_email(self):
        url = reverse_lazy('authenticate:user_me')
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data={"username":self.user.username, "password":"pass1234", "email": "bob@example.com"})
        response_json = response.json()
        print(response_json)
        self.assertEquals(response.status_code, 200, "Post request with change to email should not trigger error")

    

