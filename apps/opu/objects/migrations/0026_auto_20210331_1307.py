# Generated by Django 2.2.4 on 2021-03-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0025_auto_20210217_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalobject',
            name='comments_GOZ',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание(ГОЗ)'),
        ),
        migrations.AddField(
            model_name='object',
            name='comments_GOZ',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание(ГОЗ)'),
        ),
    ]