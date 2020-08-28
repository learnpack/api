from django.contrib import admin
from .models import CredentialsGithub, Token
# Register your models here.

@admin.register(CredentialsGithub)
class CredentialsGithubAdmin(admin.ModelAdmin):
    list_display = ('github_id', 'user', 'email', 'token')
    # fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'token_type', 'expires_at', 'user')
    def get_readonly_fields(self, request, obj=None):
        return ['key']