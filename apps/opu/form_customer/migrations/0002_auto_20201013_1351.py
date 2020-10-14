# Generated by Django 2.2.4 on 2020-10-13 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0001_initial'),
        ('form_customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='form_customer',
            name='object',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object', verbose_name='КО'),
        ),
        migrations.AddField(
            model_name='form_customer',
            name='signalization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cust_sign', to='form_customer.Signalization'),
        ),
    ]
