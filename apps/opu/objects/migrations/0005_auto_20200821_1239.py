# Generated by Django 2.2.4 on 2020-08-21 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0004_auto_20200821_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='tpo1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_tpo', to='objects.TPO'),
        ),
        migrations.AlterField(
            model_name='object',
            name='tpo2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_tpo2', to='objects.TPO'),
        ),
    ]