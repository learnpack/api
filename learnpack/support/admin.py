import requests, base64, re, json
from django.contrib import admin
from django.contrib import messages
from .models import FAQQuestion
from django.db import models
from martor.widgets import AdminMartorWidget
# Register your models here.


def mark_as_published(modeladmin, request, queryset):
    for a in queryset:
        a.status = 'PUBLISHED'
        a.save()
mark_as_published.short_description = "Mark as PUBLISHED"

def mark_as_draft(modeladmin, request, queryset):
    for a in queryset:
        a.status = 'DRAFT'
        a.save()
mark_as_draft.short_description = "Mark as DRAFT"

def mark_as_hidden(modeladmin, request, queryset):
    for a in queryset:
        a.status = 'HIDDEN'
        a.save()
mark_as_hidden.short_description = "Mark as HIDDEN"

@admin.register(FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'status', 'language')
    actions=[mark_as_published, mark_as_draft, mark_as_hidden]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }