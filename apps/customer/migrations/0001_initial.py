# Generated by Django 2.2.4 on 2020-03-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=250, null=True, verbose_name='Название')),
                ('abr', models.CharField(blank=True, max_length=100, null=True, verbose_name='Абревиатура')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес')),
                ('email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Email')),
                ('adding', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ответственное лицо')),
                ('reuisits', models.CharField(blank=True, max_length=200, null=True, verbose_name='Реквизиты')),
                ('our_services_to', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наши услуги')),
                ('connection_points', models.CharField(blank=True, max_length=200, null=True, verbose_name='Точки подключения')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Арендатор',
                'verbose_name_plural': 'Арендаторы',
            },
        ),
    ]
