# Generated by Django 2.2.4 on 2021-04-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0020_auto_20210415_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form61',
            name='outfits',
            field=models.ManyToManyField(blank=True, related_name='form61', to='objects.Outfit'),
        ),
    ]