# Generated by Django 2.2.4 on 2020-05-06 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatching', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='address',
            field=models.CharField(blank=True, max_length=355, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='request',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='request',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.DepartmentKT', verbose_name='Отдел'),
        ),
        migrations.AlterField(
            model_name='request',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя заявителя'),
        ),
        migrations.AlterField(
            model_name='request',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия заявителя'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatching.Status', verbose_name='Статус заявка'),
        ),
        migrations.AlterField(
            model_name='request',
            name='type_of_applicant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatching.TypeOfApplicant', verbose_name='Вид заявителя'),
        ),
        migrations.AlterField(
            model_name='request',
            name='type_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatching.TypeRequest', verbose_name='Тип заявки'),
        ),
    ]
