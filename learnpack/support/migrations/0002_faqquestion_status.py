# Generated by Django 3.1.6 on 2021-02-07 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqquestion',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('HIDDEN', 'Hidden')], default='DRAFT', max_length=15),
        ),
    ]
