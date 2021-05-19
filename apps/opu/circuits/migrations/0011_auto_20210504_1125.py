# Generated by Django 2.2.4 on 2021-05-04 11:25

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0031_bridge_transit'),
        ('circuits', '0010_auto_20210210_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='CircuitTransit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_trassa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='circuit_transit', to='objects.Transit')),
                ('trassa', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='transits', to='circuits.Circuit')),
            ],
        ),
        migrations.AddField(
            model_name='circuit',
            name='trassa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circuits', to='circuits.CircuitTransit'),
        ),
        migrations.AddField(
            model_name='historicalcircuit',
            name='trassa',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='circuits.CircuitTransit'),
        ),
    ]