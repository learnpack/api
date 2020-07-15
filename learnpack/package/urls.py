from django.contrib import admin
from django.urls import path, include
from .views import get_packages, get_by_slug
# from rest_framework.authtoken import views

app_name='events'
urlpatterns = [
    path('', get_packages),
    path('<str:slug>', get_by_slug),
]

