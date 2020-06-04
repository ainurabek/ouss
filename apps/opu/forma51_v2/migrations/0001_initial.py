# Generated by Django 2.2.4 on 2020-05-27 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('form51', '0001_initial'),
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(blank=True, max_length=255, null=True, verbose_name='Напр.основ.пути')),
                ('amount_inst_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество монтированных каналов')),
                ('amount_inv_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество задействованных каналов')),
                ('year', models.CharField(blank=True, max_length=100, null=True, verbose_name='Год ввода')),
                ('reserve', models.BooleanField(blank=True, null=True, verbose_name='Наличие резерва')),
                ('order', models.CharField(blank=True, max_length=255, null=True, verbose_name='Распоряжение')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forma51_v2.Category_Form')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='form51.Region')),
            ],
            options={
                'verbose_name': 'Форма 5.1',
                'verbose_name_plural': 'Форма 5.1.',
            },
        ),
    ]
