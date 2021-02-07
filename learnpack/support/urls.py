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
    FAQQuestionView
)
from rest_framework.authtoken import views

from learnpack.authenticate import templates

app_name='support'

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('question', FAQQuestionView.as_view(), name="question"),
    path('question/<str:slug>/<str:lang>', FAQQuestionView.as_view(), name="question_slug_lang"),
    path('question/<str:slug>', FAQQuestionView.as_view(), name="question_slug_lang"),
]


