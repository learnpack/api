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
class PackageTestSuite(TestCase):
    """
    Endpoint tests for Invites
    """
    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.user.set_password('pass1234')
        self.token, created = Token.objects.get_or_create(user=self.user, token_type="login")
        self.user.save()

        self.client = APIClient()
        self.package = mixer.blend("package.Package")
        self.package.save()

    def test_post_or_put_not_active(self):
        url = reverse_lazy("package:unspecified_package")
        print(url)
        response = self.client.post(url, data={"slug":"python_conditionals", "title":"Password Conditionals", "repository": "https://aa131184-73fa-4af1-aa96-4345e0d6d184.ws-us02.gitpod.io/#/workspace/api"})
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, 401, "Post request should return error if user's email isn't validated")



    def test_get_specific_package(self):
        print(self.package.slug, "SLUG")
        url = reverse_lazy('package:specific_package', kwargs={"slug":self.package.slug})
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        response_json = response.json()
        num = 0
        for item in response_json.keys():
            if item == "repository":
                num += 1
        print(response_json)
        self.assertEqual(num, 1, "Getting a specific package should return only one package")

        
    def test_post_repeat_slug(self):
        url = reverse_lazy("package:unspecified_package")
        print(url)
        print("AUTHENTICATED: ", self.user.is_authenticated)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data={"slug":self.package.slug, "title":"Password Conditionals", "repository": "https://aa131184-73fa-4af1-aa96-4345e0d6d184.ws-us02.gitpod.io/#/workspace/api"})
        response_json = response.json()
        print(response_json, "RESPONSE")
        print("STATUS: ", response.status_code)
        self.assertEqual(response.status_code, 405, "Post request with repeated slug should trigger error")

    def test_get_technologies(self):
        url = reverse_lazy('package:get_technologies')
        print(self.package)
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        response_json = response.json()
        print(response_json)
        self.assertEqual(len(response_json), 1, "Getting technologies should return a single technology, as only one technology exists in the setup")


    def test_get_languages(self):
        url = reverse_lazy('package:get_languages')
        print(self.package)
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        response_json = response.json()
        print(response_json)
        self.assertEqual(len(response_json), 1, "Getting languages should return a single language, as only one language exists in the setup")

    def test_get_skills(self):
        url = reverse_lazy('package:get_skills')
        print(self.package)
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        response_json = response.json()
        print(response_json)
        self.assertEqual(len(response_json), 1, "Getting skills should return a single skill, as only one skill exists in the setup")


    

