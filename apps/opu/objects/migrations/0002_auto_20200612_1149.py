# Generated by Django 2.2.4 on 2020-06-12 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='index',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='system',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Обозначение'),
        ),
    ]
