# Generated by Django 2.2.4 on 2021-04-14 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0017_auto_20210414_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form61',
            name='nodes',
        ),
        migrations.AddField(
            model_name='form61',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='analysis.Form61'),
        ),
    ]