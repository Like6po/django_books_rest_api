# Generated by Django 4.0 on 2022-08-22 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
