# Generated by Django 3.0.8 on 2020-07-15 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('slug', models.SlugField(max_length=15, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('total_packages', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('slug', models.SlugField(max_length=15, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('total_packages', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('slug', models.SlugField(max_length=150, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('readme', models.TextField(default='Empty README.md', max_length=250)),
                ('repository', models.URLField(max_length=250)),
                ('homepage', models.URLField(blank=True, default=None, max_length=250, null=True)),
                ('license_slug', models.SlugField(blank=True, default=None, max_length=10, null=True)),
                ('license_url', models.URLField(blank=True, default=None, max_length=250, null=True)),
                ('preview_image', models.URLField(blank=True, default=None, max_length=250, null=True)),
                ('preview_video', models.URLField(blank=True, default=None, max_length=250, null=True)),
                ('duration_in_hours', models.IntegerField(blank=True, default=None, null=True)),
                ('likes', models.IntegerField(default=0)),
                ('downloads', models.IntegerField(default=0)),
                ('difficulty', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('video_solutions', models.BooleanField(default=False)),
                ('graded', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='package.Language')),
                ('technology', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='package.Technology')),
            ],
        ),
    ]
