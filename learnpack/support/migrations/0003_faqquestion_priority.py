# Generated by Django 3.1.6 on 2021-02-08 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_faqquestion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqquestion',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]