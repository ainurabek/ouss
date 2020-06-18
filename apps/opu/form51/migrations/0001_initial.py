# Generated by Django 2.2.4 on 2020-06-17 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('objects', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form51',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ouss', models.CharField(blank=True, max_length=250, null=True, verbose_name='Номер распоряжения ОУСС')),
                ('order', models.ImageField(blank=True, null=True, upload_to='object/order/', verbose_name='Распоряжение')),
                ('schema', models.ImageField(blank=True, null=True, upload_to='object/schema/', verbose_name='Схема')),
                ('reserve', models.CharField(blank=True, max_length=15, null=True, verbose_name='Резерва потока')),
                ('report_num', models.CharField(blank=True, max_length=200, null=True, verbose_name='Номер донесения')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer', verbose_name='Примечание (№ID, МН, Аренда)')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object', verbose_name='КО')),
                ('reserve_object', models.ManyToManyField(blank=True, related_name='reserve_objects', to='objects.Object', verbose_name='Трасса резерва потока')),
            ],
            options={
                'verbose_name': 'Форма 5.1',
                'verbose_name_plural': 'Форма 5.1.',
            },
        ),
    ]
