# Generated by Django 2.2.4 on 2020-08-20 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form51', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='slug',
        ),
    ]
