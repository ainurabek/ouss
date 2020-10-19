# Generated by Django 2.2.4 on 2020-10-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_auto_20201013_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagecoef',
            name='punkt5_country',
            field=models.FloatField(blank=True, null=True, verbose_name='Расчет коэф.качества по ЛКХ (п.5.Респ)'),
        ),
        migrations.AlterField(
            model_name='averagecoef',
            name='punkt7_country',
            field=models.FloatField(blank=True, null=True, verbose_name='Расчет коэф.качества по ЛКХ (п.7.Респ)'),
        ),
        migrations.AlterField(
            model_name='averagecoef',
            name='total_coefficient_punkt5',
            field=models.FloatField(blank=True, null=True, verbose_name='Расчет коэф.качества по ЛКХ (п.7)'),
        ),
        migrations.AlterField(
            model_name='averagecoef',
            name='total_coefficient_punkt7',
            field=models.FloatField(blank=True, null=True, verbose_name='Расчет коэф.качества по ЛКХ (п.7)'),
        ),
    ]
