# Generated by Django 2.2.4 on 2021-05-04 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0031_bridge_transit'),
    ]

    operations = [
        migrations.AddField(
            model_name='transit',
            name='create_circuit_transit',
            field=models.BooleanField(default=False),
        ),
    ]