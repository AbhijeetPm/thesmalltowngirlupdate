# Generated by Django 3.1.6 on 2021-06-21 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_app', '0002_profile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_main',
        ),
    ]