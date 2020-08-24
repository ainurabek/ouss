# Generated by Django 2.2.4 on 2020-08-21 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0009_auto_20200820_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contact_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.OutfitWorker', verbose_name='Передал (ФИО)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile', verbose_name='ФИО диспетчера'),
        ),
        migrations.AlterField(
            model_name='event',
            name='point1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='point1_event', to='objects.Point', verbose_name='Ип от'),
        ),
        migrations.AlterField(
            model_name='event',
            name='point2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='point2_event', to='objects.Point', verbose_name='Ип до'),
        ),
        migrations.AlterField(
            model_name='event',
            name='reason',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dispatching.Reason', verbose_name='Причины'),
        ),
        migrations.AlterField(
            model_name='event',
            name='responsible_outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dispatch_outfit', to='objects.Outfit', verbose_name='Ответственный'),
        ),
        migrations.AlterField(
            model_name='event',
            name='send_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dispatch_send_outfit', to='objects.Outfit', verbose_name='Передал (предприятие)'),
        ),
    ]