# Generated by Django 2.2.4 on 2021-07-21 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0036_remove_transit_is_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpoint',
            name='total_point_channels_KLS',
        ),
        migrations.RemoveField(
            model_name='historicalpoint',
            name='total_point_channels_RRL',
        ),
        migrations.RemoveField(
            model_name='point',
            name='total_point_channels_KLS',
        ),
        migrations.RemoveField(
            model_name='point',
            name='total_point_channels_RRL',
        ),
    ]