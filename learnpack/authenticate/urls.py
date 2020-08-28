"""learnpack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    get_users, UserMeView, get_groups, CustomAuthToken, get_github_token, save_github_token, UserView, sign_up,
    EmailView, ValidateEmailView)
from rest_framework.authtoken import views
from learnpack.package.views import UnspecifiedPackageView, get_languages, get_technologies, PackageView
from django.contrib.auth import views as auth_views
from learnpack.authenticate import templates

app_name='authenticate'
urlpatterns = [
    path('user/', get_users, name="user"),
    path('user/me', UserMeView.as_view(), name="user_me"),
    path('group/', get_groups),
    path('token/', CustomAuthToken.as_view()),
    path('signup/', sign_up, name="sign_up"),
    path('<str:id>', UserView.as_view(), name= "particular_user_view"),
    path('email/validate/<str:token>', ValidateEmailView.as_view(), name="token"),
    path('test_template/<str:slug>', EmailView.as_view()),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='change_password.html',
            success_url = '/'), name= "change_password"),
    path('github/', get_github_token),
    path('github/callback/', save_github_token),
]

