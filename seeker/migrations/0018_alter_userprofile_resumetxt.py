# Generated by Django 3.2.4 on 2023-08-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeker', '0017_auto_20230810_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='resumetxt',
            field=models.CharField(default='', max_length=1048550),
        ),
    ]
