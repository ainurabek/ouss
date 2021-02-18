# Generated by Django 2.2.4 on 2021-02-10 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0009_auto_20210119_1240'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Speed',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='measure',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='mode',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='speed',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='type_com',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='type_using',
        ),
        migrations.RemoveField(
            model_name='historicalcircuit',
            name='measure',
        ),
        migrations.RemoveField(
            model_name='historicalcircuit',
            name='mode',
        ),
        migrations.RemoveField(
            model_name='historicalcircuit',
            name='speed',
        ),
        migrations.RemoveField(
            model_name='historicalcircuit',
            name='type_com',
        ),
        migrations.RemoveField(
            model_name='historicalcircuit',
            name='type_using',
        ),
        migrations.DeleteModel(
            name='Measure',
        ),
        migrations.DeleteModel(
            name='Mode',
        ),
        migrations.DeleteModel(
            name='TypeCom',
        ),
    ]