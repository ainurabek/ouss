# Generated by Django 2.2.4 on 2020-08-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0013_event_time_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_period',
            field=models.TimeField(blank=True, null=True, verbose_name='Сумма часов, за которое устранили аварию'),
        ),
    ]