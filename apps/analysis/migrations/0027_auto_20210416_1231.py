# Generated by Django 2.2.4 on 2021-04-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0026_auto_20210415_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='parent',
        ),
        migrations.AddField(
            model_name='station',
            name='parent',
            field=models.ManyToManyField(blank=True, related_name='nodes', to='analysis.Station'),
        ),
    ]