# Generated by Django 2.2.4 on 2021-05-31 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_customer', '0006_auto_20210412_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form_customer',
            name='circuit',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_cust_cir', to='circuits.Circuit', verbose_name='Каналы'),
        ),
        migrations.AlterField(
            model_name='form_customer',
            name='object',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_cust_obj', to='objects.Object', verbose_name='КО'),
        ),
    ]
