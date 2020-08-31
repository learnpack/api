from test.support import EnvironmentVarGuard # Python >=3
from django.test import TestCase, override_settings
from django.apps import apps
from learnpack.package import urls
from django.conf import settings
import os
from django.urls.base import reverse_lazy, reverse
from mixer.backend.django import mixer
from rest_framework.test import force_authenticate, APIClient
from django.contrib.auth.models import User, Group
from learnpack.package.models import Package


# Create your tests here.
class PackageTestSuite(TestCase):
    """
    Endpoint tests for Invites
    """
    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.user.set_password('pass1234')
        self.user.save()

        self.package = mixer.blend("package.Package")
        self.package.save()

    def test_post_or_put_not_active(self):
        url = reverse_lazy("package:unspecified_package", current_app = "package")
        print(url)
        response = self.client.post(url, data={"slug":"python_conditionals", "title":"Password Conditionals", "repository": "https://aa131184-73fa-4af1-aa96-4345e0d6d184.ws-us02.gitpod.io/#/workspace/api"})
        response_json = response.json()
        print(response_json)
        self.assertEquals(response.status_code, 401, "Post request should return error if user's email isn't validated")



    def test_get_specific_package(self):
        print(self.package.slug, "SLUG")
        url = reverse_lazy('package:specific_package', kwargs={"slug":self.package.slug})
        print(url)
        response = self.client.get(url)
        response_json = response.json()
        print(response_json)
        self.assertEquals(len(response_json), 1, "Getting a specific package should return only one package")
