# Generated by Django 3.0.8 on 2021-02-03 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0005_auto_20201126_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='package',
            name='skills',
        ),
        migrations.AddField(
            model_name='package',
            name='skills',
            field=models.ManyToManyField(null=True, to='package.Skill'),
        ),
    ]
