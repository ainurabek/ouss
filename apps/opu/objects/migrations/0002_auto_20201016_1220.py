# Generated by Django 2.2.4 on 2020-10-16 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='point_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_point', to='objects.Point'),
        ),
    ]
