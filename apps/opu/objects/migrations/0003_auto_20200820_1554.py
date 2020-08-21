# Generated by Django 2.2.4 on 2020-08-20 09:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='index',
            field=models.CharField(max_length=100, verbose_name='Индекс'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Обозначение'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inout',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ip',
            name='object_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_object', to='objects.Object'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ip',
            name='point_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_point', to='objects.Point'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='linetype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outfit',
            name='adding',
            field=models.CharField( max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outfitworker',
            name='name',
            field=models.CharField( max_length=100, verbose_name='ФИО'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outfitworker',
            name='outfit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outfit_worker', to='objects.Outfit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='point',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='point',
            name='point',
            field=models.CharField( max_length=100, verbose_name='ИП'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='system',
            name='name',
            field=models.CharField( max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tpo',
            name='index',
            field=models.CharField( max_length=100, verbose_name='Индекс'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tpo',
            name='name',
            field=models.CharField( max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='typeoftrakt',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
