# Generated by Django 5.1.3 on 2024-11-16 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_userpreferences_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPreferences',
        ),
    ]