# Generated by Django 2.2.4 on 2020-08-21 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200820_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_profile_created',
            field=models.BooleanField(default=False, verbose_name='Создан ли профиль'),
        ),
    ]