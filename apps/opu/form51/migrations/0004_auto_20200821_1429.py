# Generated by Django 2.2.4 on 2020-08-21 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form51', '0003_remove_region_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form51',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile'),
        ),
    ]
