from django.contrib import admin
from django.urls import path, include
from .views import get_packages, get_by_slug, get_technologies, get_languages
# from rest_framework.authtoken import views

app_name='events'
urlpatterns = [
    path('', get_packages),
    path('technology', get_technologies),
    path('language', get_languages),
    path('<str:slug>', get_by_slug),
]

