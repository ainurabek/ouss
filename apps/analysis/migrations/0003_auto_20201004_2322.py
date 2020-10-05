# Generated by Django 2.2.4 on 2020-10-04 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_auto_20201004_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punkt5',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='punkt5_event', to='dispatching.Event'),
        ),
        migrations.AlterField(
            model_name='punkt5',
            name='outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='punkt5_outfit', to='objects.Outfit'),
        ),
    ]
