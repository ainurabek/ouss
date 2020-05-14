# Generated by Django 2.2.4 on 2020-05-06 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('dispatching', '0002_auto_20200506_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='subdepartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.SubdepartmentKT', verbose_name='Подотдел'),
        ),
    ]