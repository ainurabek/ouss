# Generated by Django 2.2.4 on 2021-08-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='bypass',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='bypass',
            field=models.BooleanField(default=False),
        ),
    ]
