# Generated by Django 2.2.4 on 2021-04-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0030_auto_20210429_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodlaying',
            name='is_read_only',
            field=models.BooleanField(default=False),
        ),
    ]