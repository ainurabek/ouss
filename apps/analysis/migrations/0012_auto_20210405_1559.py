# Generated by Django 2.2.4 on 2021-04-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0011_auto_20210405_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='punkt5',
            name='formula_activate',
        ),
        migrations.AddField(
            model_name='punkt5',
            name='length_kls',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км КЛС'),
        ),
        migrations.AddField(
            model_name='punkt5',
            name='length_rrl',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км РРЛ'),
        ),
        migrations.AddField(
            model_name='punkt5',
            name='length_vls',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Протяженность кан*км ВЛС'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='corresponding_norm_kls',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме КЛС'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='corresponding_norm_rrl',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме РРЛ'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='corresponding_norm_vls',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Соответствующих норме ВЛС'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='total_number_kls',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов КЛС'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='total_number_rrl',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов РРЛ'),
        ),
        migrations.AddField(
            model_name='punkt7',
            name='total_number_vls',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Общее количество линейных трактов ВЛС'),
        ),
    ]