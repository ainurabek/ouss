# Generated by Django 2.2.4 on 2020-08-24 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0010_auto_20200821_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('id',), 'verbose_name': 'Журнал событий', 'verbose_name_plural': 'Журнал событий'},
        ),
    ]