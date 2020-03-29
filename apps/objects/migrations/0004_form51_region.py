# Generated by Django 2.2.4 on 2020-03-29 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('objects', '0003_auto_20200328_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Область',
                'verbose_name_plural': 'Список областей',
            },
        ),
        migrations.CreateModel(
            name='Form51',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер задейственного канала')),
                ('direction', models.CharField(blank=True, max_length=100, null=True, verbose_name='Направление основного пути')),
                ('amount_inst_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество монтированных каналов')),
                ('amount_inv_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество задействованных каналов')),
                ('year', models.CharField(blank=True, max_length=100, null=True, verbose_name='Год ввода')),
                ('order', models.ImageField(blank=True, upload_to='object/order/', verbose_name='Распоряжение')),
                ('schema', models.ImageField(blank=True, upload_to='object/schema/', verbose_name='Схема')),
                ('reserve', models.BooleanField(blank=True, null=True, verbose_name='Наличие резерва')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_form51', to='customer.Customer')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_form51', to='objects.Region')),
                ('trassa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trassa_form51', to='objects.Trassa')),
            ],
            options={
                'verbose_name': 'Форма 5.1',
                'verbose_name_plural': 'Форма 5.1.',
            },
        ),
    ]
