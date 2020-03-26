# Generated by Django 2.2.4 on 2020-03-11 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_auto_20200311_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='tpo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.TPO'),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='type_outfit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.TypeOfLocation'),
        ),
    ]