# Generated by Django 2.2.4 on 2020-04-19 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_remove_object_add_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='add_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
