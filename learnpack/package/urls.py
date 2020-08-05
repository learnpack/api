from django.contrib import admin
from django.urls import path, include
from .views import PackageView, get_technologies, get_languages, UnspecifiedPackageView
# from rest_framework.authtoken import views

app_name='events'
urlpatterns = [
    path('', UnspecifiedPackageView.as_view()),
    path('technology', get_technologies),
    path('language', get_languages),
    path('<str:slug>', PackageView.as_view()),
]

