# Generated by Django 2.2.4 on 2020-10-19 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
        ('accounts', '0001_initial'),
        ('analysis', '0024_auto_20201016_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Punkt5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outfit_period_of_time_kls', models.FloatField(blank=True, default=0, null=True, verbose_name='Продолжительность всех ПВ кан*час КЛС')),
                ('length_kls', models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км КЛС')),
                ('downtime_kls', models.FloatField(blank=True, default=0, null=True, verbose_name='Простои КЛС')),
                ('coefficient_kls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества КЛС')),
                ('outfit_period_of_time_vls', models.FloatField(blank=True, default=0, null=True, verbose_name='Продолжительность всех ПВ кан*час ВЛС')),
                ('length_vls', models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км ВЛС')),
                ('downtime_vls', models.FloatField(blank=True, default=0, null=True, verbose_name='Простои ВЛС')),
                ('coefficient_vls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества ВЛС')),
                ('outfit_period_of_time_rrl', models.FloatField(blank=True, default=0, null=True, verbose_name='Продолжительность всех ПВ кан*час РРЛ')),
                ('length_rrl', models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км РРЛ')),
                ('downtime_rrl', models.FloatField(blank=True, default=0, null=True, verbose_name='Простои РРЛ')),
                ('coefficient_rrl', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества РРЛ')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='Начало')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='Конец')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.Outfit', verbose_name='Предприятия')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'п.5',
                'verbose_name_plural': 'п.5',
            },
        ),
        migrations.CreateModel(
            name='Punkt7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_number_kls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов КЛС')),
                ('corresponding_norm_kls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме КЛС')),
                ('percentage_compliance_kls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Процент соответствия КЛС')),
                ('coefficient_kls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества КЛС')),
                ('total_number_vls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов ВЛС')),
                ('corresponding_norm_vls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме ВЛС')),
                ('percentage_compliance_vls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Процент соответствия ВЛС')),
                ('coefficient_vls', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества')),
                ('total_number_rrl', models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов РРЛ')),
                ('corresponding_norm_rrl', models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме РРЛ')),
                ('percentage_compliance_rrl', models.IntegerField(blank=True, default=0, null=True, verbose_name='Процент соответствия РРЛ')),
                ('coefficient_rrl', models.IntegerField(blank=True, default=0, null=True, verbose_name='Коэффициент качества РРЛ')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='Начало')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='Конец')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.Outfit', verbose_name='Предприятия')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'п.7',
                'verbose_name_plural': 'п.7',
            },
        ),
        migrations.RemoveField(
            model_name='item7',
            name='outfit_item',
        ),
        migrations.RemoveField(
            model_name='item7',
            name='type_line',
        ),
        migrations.RemoveField(
            model_name='item7',
            name='user',
        ),
        migrations.RemoveField(
            model_name='outfititem',
            name='analysis_form_item5',
        ),
        migrations.RemoveField(
            model_name='outfititem',
            name='analysis_form_item7',
        ),
        migrations.RemoveField(
            model_name='outfititem',
            name='id_parent',
        ),
        migrations.RemoveField(
            model_name='outfititem',
            name='outfit',
        ),
        migrations.RemoveField(
            model_name='typelinevalue',
            name='total_data',
        ),
        migrations.RemoveField(
            model_name='typelinevalue',
            name='type_line',
        ),
        migrations.RenameField(
            model_name='totaldata',
            old_name='coefficient',
            new_name='total_coefficient',
        ),
        migrations.RemoveField(
            model_name='totaldata',
            name='id_parent',
        ),
        migrations.RemoveField(
            model_name='totaldata',
            name='outfit',
        ),
        migrations.AddField(
            model_name='formanalysis',
            name='tv_coefficient',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Коэффициент качества ТВ'),
        ),
        migrations.AddField(
            model_name='totaldata',
            name='kls',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Значение'),
        ),
        migrations.AddField(
            model_name='totaldata',
            name='rrl',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Значение'),
        ),
        migrations.AddField(
            model_name='totaldata',
            name='vls',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Значение'),
        ),
        migrations.DeleteModel(
            name='Item5',
        ),
        migrations.DeleteModel(
            name='Item7',
        ),
        migrations.DeleteModel(
            name='OutfitItem',
        ),
        migrations.DeleteModel(
            name='TypeLineValue',
        ),
        migrations.AddField(
            model_name='formanalysis',
            name='punkt5',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_analysis5', to='analysis.Punkt5', verbose_name='Форма анализа'),
        ),
        migrations.AddField(
            model_name='formanalysis',
            name='punkt7',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_analysis7', to='analysis.Punkt7', verbose_name='Форма анализа'),
        ),
        migrations.AddField(
            model_name='totaldata',
            name='punkt5',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='total_data5', to='analysis.Punkt5'),
        ),
        migrations.AddField(
            model_name='totaldata',
            name='punkt7',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='total_data7', to='analysis.Punkt7'),
        ),
    ]
