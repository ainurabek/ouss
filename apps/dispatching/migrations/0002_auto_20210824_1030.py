# Generated by Django 2.2.4 on 2021-08-24 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_auto_20210823_1430'),
        ('dispatching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='iptv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_iptv', to='objects.IPTV', verbose_name='Каналы IPTV'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='iptv',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='objects.IPTV', verbose_name='Каналы IPTV'),
        ),
    ]