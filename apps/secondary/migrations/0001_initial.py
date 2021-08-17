# Generated by Django 2.2.4 on 2021-08-17 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип станции',
                'verbose_name_plural': 'Тип станции',
            },
        ),
        migrations.CreateModel(
            name='SecondaryBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_launch', models.CharField(blank=True, max_length=500, null=True, verbose_name='Год запуска')),
                ('installed_value', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Монтированная емкость')),
                ('active_value', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Задействованная емкость')),
                ('active_numbering', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Задействованная нумерация')),
                ('free_numbering', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Свободная нумерация')),
                ('GAS_numbering', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Выделенная ГАС нумерация')),
                ('GAS_return', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Возврат в ГАС')),
                ('KT_numbering', models.FloatField(blank=True, default=0, null=True, verbose_name='Нумерация КТ')),
                ('comments', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Примечание')),
                ('created_at', models.DateField(blank=True, null=True, verbose_name='Дата создания')),
                ('administrative_division', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Примечание')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile', verbose_name='ФИО диспетчера')),
                ('outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_out', to='objects.Outfit')),
                ('point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='point_secondary', to='objects.Point', verbose_name='ИП')),
                ('type_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_station_second', to='secondary.TypeStation')),
            ],
            options={
                'verbose_name': 'База вторичной сети',
                'verbose_name_plural': 'База вторичной сети',
                'ordering': ('id',),
                'get_latest_by': 'id',
            },
        ),
    ]
