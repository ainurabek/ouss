# Generated by Django 2.2.4 on 2020-06-02 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_auto_20200602_1207'),
        ('circuits', '0005_auto_20200602_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuit',
            name='final_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_final_dest', to='objects.Point'),
        ),
        migrations.AlterField(
            model_name='circuit',
            name='first',
            field=models.BooleanField(blank=True, null=True, verbose_name='Используется/Не используется'),
        ),
    ]