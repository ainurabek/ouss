# Generated by Django 2.2.4 on 2020-08-24 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0009_auto_20200824_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='object',
            options={'ordering': ('id',), 'verbose_name': 'Линия передачи/Обьект/Тракт', 'verbose_name_plural': 'Линия передачи/Обьект/Тракт'},
        ),
    ]