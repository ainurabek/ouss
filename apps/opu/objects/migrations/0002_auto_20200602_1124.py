# Generated by Django 2.2.4 on 2020-06-02 05:24

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='transit',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, null=True, related_name='transit_obj1', to='objects.Object'),
        ),
        migrations.AlterField(
            model_name='object',
            name='transit2',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, null=True, related_name='transit_obj2', to='objects.Object'),
        ),
    ]