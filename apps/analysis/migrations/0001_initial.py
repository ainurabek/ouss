# Generated by Django 2.2.4 on 2020-10-13 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_Coefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_punkt5', models.FloatField(blank=True, null=True, verbose_name='Общая протяж.кан*км')),
                ('KLS', models.FloatField(blank=True, null=True, verbose_name='КЛС')),
                ('RRL', models.FloatField(blank=True, null=True, verbose_name='РРЛ')),
                ('VLS', models.FloatField(blank=True, null=True, verbose_name='ВЛС')),
                ('total_coefficient', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
            ],
            options={
                'verbose_name': 'Удельный вес протяженности',
                'verbose_name_plural': 'Удельный вес протяженности',
            },
        ),
        migrations.CreateModel(
            name='AverageCoef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient_quality_tv', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (ТВ)')),
                ('avg_coefficient', models.FloatField(blank=True, null=True, verbose_name='Средний коэффициент качества')),
                ('avg_coefficient_country', models.FloatField(blank=True, null=True, verbose_name='Средний коэффициент качества по республике')),
                ('target_coefficient', models.FloatField(blank=True, null=True, verbose_name='Нормативный коэффициент качества')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
            ],
            options={
                'verbose_name': 'Средний коффициент качества',
                'verbose_name_plural': 'Средний коффициент качества',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Название')),
                ('punkt5_total_outfit_vls', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(ВЛС)')),
                ('total_outfit_region_vls', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(ВЛС)')),
                ('stops_vls', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (ВЛС)')),
                ('coefficient_vls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('punkt5_total_outfit_kls', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(КЛС)')),
                ('total_outfit_region_kls', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(КЛС)')),
                ('stops_kls', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (КЛС)')),
                ('coefficient_kls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (КЛС)')),
                ('punkt5_total_outfit_rrl', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(РРЛ)')),
                ('total_outfit_region_rrl', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(РРЛ)')),
                ('stops_rrl', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (РРЛ)')),
                ('coefficient_rrl', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('total_punkt5', models.FloatField(blank=True, null=True, verbose_name='Общая протяж.кан*км')),
                ('KLS', models.FloatField(blank=True, null=True, verbose_name='КЛС')),
                ('RRL', models.FloatField(blank=True, null=True, verbose_name='РРЛ')),
                ('VLS', models.FloatField(blank=True, null=True, verbose_name='ВЛС')),
                ('total_coefficient', models.FloatField(blank=True, null=True)),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
            ],
            options={
                'verbose_name': 'Общая республика',
                'verbose_name_plural': 'Общая республика',
            },
        ),
        migrations.CreateModel(
            name='Country_Punkt7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Название')),
                ('line_trakt_outfit_kls', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(КЛС)')),
                ('line_trakt_outfit_vls', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(ВЛС)')),
                ('line_trakt_outfit_rrl', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(РРЛ)')),
                ('norm_KLS', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(КЛС)')),
                ('norm_VLS', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(ВЛС)')),
                ('norm_RRL', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(РРЛ)')),
                ('percent_accordance_KLS', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(КЛС)')),
                ('percent_accordance_VLS', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(ВЛС)')),
                ('percent_accordance_RRL', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(РРЛ)')),
                ('coefficient_kls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (КЛС)')),
                ('coefficient_rrl', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('coefficient_vls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
                ('KLS', models.FloatField(blank=True, null=True, verbose_name='КЛС')),
                ('RRL', models.FloatField(blank=True, null=True, verbose_name='РРЛ')),
                ('VLS', models.FloatField(blank=True, null=True, verbose_name='ВЛС')),
                ('total_coefficient', models.FloatField(blank=True, null=True)),
                ('total_amount_trakts', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов')),
            ],
            options={
                'verbose_name': 'Пункт №7(Республика)',
                'verbose_name_plural': 'Пункт №7(Республика)',
            },
        ),
        migrations.CreateModel(
            name='FormAK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punkt5_total_outfit_kls', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(КЛС)')),
                ('punkt5_total_outfit_rrl', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(РРЛ)')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
                ('created_at', models.DateField(blank=True, null=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Форма АК',
                'verbose_name_plural': 'Форма АК',
            },
        ),
        migrations.CreateModel(
            name='Punkt5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Название')),
                ('punkt5_total_outfit_vls', models.FloatField(blank=True, null=True, verbose_name='Продолжительность всех ПВ кан*час(ВЛС)')),
                ('country_punkt5_total', models.FloatField(blank=True, max_length=500, null=True, verbose_name='Республика')),
                ('total_outfit_region_kls', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(КЛС)')),
                ('total_outfit_region_rrl', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(РРЛ)')),
                ('total_outfit_region_vls', models.FloatField(blank=True, null=True, verbose_name='Протяженность кан*км зад.(ВЛС)')),
                ('stops_kls', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (КЛС)')),
                ('stops_rrl', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (РРЛ)')),
                ('stops_vls', models.FloatField(blank=True, null=True, verbose_name='Простои на 1000 кан*км (ВЛС)')),
                ('coefficient_kls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (КЛС)')),
                ('coefficient_rrl', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('coefficient_vls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
            ],
            options={
                'verbose_name': 'Пункт №5',
                'verbose_name_plural': 'Пункт №5',
            },
        ),
        migrations.CreateModel(
            name='Punkt7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_trakt_outfit_kls', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(КЛС)')),
                ('line_trakt_outfit_vls', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(ВЛС)')),
                ('line_trakt_outfit_rrl', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов(РРЛ)')),
                ('norm_KLS', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(КЛС)')),
                ('norm_VLS', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(ВЛС)')),
                ('norm_RRL', models.IntegerField(blank=True, null=True, verbose_name='в т.ч. соответствующих норме(РРЛ)')),
                ('percent_accordance_KLS', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(КЛС)')),
                ('percent_accordance_VLS', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(ВЛС)')),
                ('percent_accordance_RRL', models.FloatField(blank=True, null=True, verbose_name='Процент соответствия(РРЛ)')),
                ('coefficient_kls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (КЛС)')),
                ('coefficient_rrl', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('coefficient_vls', models.FloatField(blank=True, null=True, verbose_name='Коэффициент качества (РРЛ)')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='До')),
                ('KLS', models.FloatField(blank=True, null=True, verbose_name='КЛС')),
                ('RRL', models.FloatField(blank=True, null=True, verbose_name='РРЛ')),
                ('VLS', models.FloatField(blank=True, null=True, verbose_name='ВЛС')),
                ('total_coefficient', models.FloatField(blank=True, null=True)),
                ('total_amount_trakts', models.IntegerField(blank=True, null=True, verbose_name='Общее количество линейных трактов')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_punkt7', to='analysis.Country_Punkt7')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile', verbose_name='ФИО создателя')),
            ],
            options={
                'verbose_name': 'Пункт №7',
                'verbose_name_plural': 'Пункт №7',
            },
        ),
    ]
