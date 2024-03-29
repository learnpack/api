# Generated by Django 3.1.6 on 2021-02-07 22:00

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQQuestion',
            fields=[
                ('slug', models.SlugField(max_length=150, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('answer', martor.models.MartorField(blank=True, default=None, null=True)),
                ('language', models.CharField(default='us', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
