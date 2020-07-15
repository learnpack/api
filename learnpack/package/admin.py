import requests, base64, re, json
from django.contrib import admin
from django.contrib import messages
from .models import Package, Technology, Language
# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'duration_in_hours')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    actions = []