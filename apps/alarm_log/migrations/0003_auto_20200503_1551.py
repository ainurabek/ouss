# Generated by Django 2.2.4 on 2020-05-03 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('form51', '0003_auto_20200420_1403'),
        ('alarm_log', '0002_auto_20200503_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShutdownType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Вид отключения',
                'verbose_name_plural': 'Виды отключений',
            },
        ),
        migrations.AlterField(
            model_name='statement',
            name='address',
            field=models.CharField(max_length=355, verbose_name='Адрес'),
        ),
        migrations.CreateModel(
            name='ShutdownLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=355, verbose_name='Адрес')),
                ('сause', models.CharField(max_length=355, verbose_name='Причина')),
                ('shutdown_periods_from', models.DateTimeField(verbose_name='Период отключения от')),
                ('shutdown_periods_to', models.DateTimeField(verbose_name='Период отключения до')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form51.Region', verbose_name='Регион')),
                ('shutdown_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_log.ShutdownType', verbose_name='Вид отключения')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_log.Status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Журнал отключения',
                'verbose_name_plural': 'Журнал отключений',
            },
        ),
    ]
