# Generated by Django 2.2.4 on 2020-08-24 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0011_auto_20200824_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Журнал событий', 'verbose_name_plural': 'Журнал событий'},
        ),
    ]