from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Package(models.Model):
    slug = models.SlugField(max_length=150, primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True, default=None)
    readme = models.TextField(max_length=250,default='Empty README.md')

    repository = models.URLField(max_length=250)
    homepage = models.URLField(max_length=250, blank=True,null=True, default=None)
    
    license_slug = models.SlugField(max_length=10, blank=True, null=True, default=None)
    license_url = models.URLField(max_length=250, blank=True, null=True, default=None)
    
    preview_image = models.URLField(max_length=250, blank=True, null=True, default=None)
    preview_video = models.URLField(max_length=250, blank=True, null=True, default=None)
    
    duration_in_hours = models.IntegerField(blank=True, null=True, default=None)
    likes = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    
    difficulty = models.CharField(max_length=30, blank=True,null=True, default=None)
    video_solutions = models.BooleanField(default=False)
    graded = models.BooleanField(default=False)

    technology = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)
    language = models.ForeignKey('Technology',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title

class Language(models.Model):
    slug = models.SlugField(max_length=15, primary_key=True)
    title = models.CharField(max_length=150)
    total_packages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Technology(models.Model):
    slug = models.SlugField(max_length=15, primary_key=True)
    title = models.CharField(max_length=150)
    total_packages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title