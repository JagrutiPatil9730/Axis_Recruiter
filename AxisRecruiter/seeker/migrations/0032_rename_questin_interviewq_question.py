# Generated by Django 3.2.4 on 2023-08-14 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seeker', '0031_auto_20230814_0856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interviewq',
            old_name='Questin',
            new_name='Question',
        ),
    ]
