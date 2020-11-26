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
    UnspecifiedPackageView, get_technologies, get_languages, PackageView, get_skills,
    PostPackageView
)
from rest_framework.authtoken import views

from django.contrib.auth import views as auth_views
from learnpack.authenticate import templates

app_name='package'
urlpatterns = [
    path('', PostPackageView.as_view(), name="unspecified_package"),
    path('all', UnspecifiedPackageView.as_view(), name="unspecified_package"),
    path('technology', get_technologies, name="get_technologies"),
    path('language', get_languages, name="get_languages"),
    path('skill', get_skills, name="get_skills"),
    path('<str:slug>', PackageView.as_view(), name="specific_package"),
]


