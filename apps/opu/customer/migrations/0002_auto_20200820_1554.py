# Generated by Django 2.2.4 on 2020-08-20 09:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='abr',
            field=models.CharField(max_length=100, verbose_name='Абревиатура'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer',
            field=models.CharField(max_length=250, verbose_name='Название'),
            preserve_default=False,
        ),
    ]