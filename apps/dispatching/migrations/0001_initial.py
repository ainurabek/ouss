# Generated by Django 2.2.4 on 2020-05-05 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('form51', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShutdownType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Вид отключения',
                'verbose_name_plural': 'Виды отключений',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус завки',
                'verbose_name_plural': 'Статусы заявок',
            },
        ),
        migrations.CreateModel(
            name='TypeOfApplicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Вид заявителя')),
            ],
            options={
                'verbose_name': 'Вид заявителя',
                'verbose_name_plural': 'Виды заявителей',
            },
        ),
        migrations.CreateModel(
            name='TypeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тип заявки')),
            ],
            options={
                'verbose_name': 'Тип заявки',
                'verbose_name_plural': 'Типы заявок',
            },
        ),
        migrations.CreateModel(
            name='ShutdownLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=355, verbose_name='Адрес')),
                ('сause', models.CharField(max_length=355, verbose_name='Причина')),
                ('shutdown_periods_from', models.DateTimeField(blank=True, null=True, verbose_name='Период отключения')),
                ('shutdown_periods_to', models.DateTimeField(blank=True, null=True, verbose_name='Период отключения')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form51.Region', verbose_name='Регион')),
                ('shutdown_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatching.ShutdownType', verbose_name='Вид отключения')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatching.Status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Журнал отключений',
                'verbose_name_plural': 'Журнал отключений',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=355, verbose_name='Адрес')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя заявителя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия заявителя')),
                ('telephone_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер телефона заявителя')),
                ('home_phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер домашнего телефона')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Описание проблемы')),
                ('date_from', models.DateTimeField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateTimeField(blank=True, null=True, verbose_name='До')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='Создан')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.DepartmentKT', verbose_name='Отдел')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatching.Status', verbose_name='Статус заявка')),
                ('type_of_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatching.TypeOfApplicant', verbose_name='Вид заявителя')),
                ('type_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatching.TypeRequest', verbose_name='Тип заявки')),
            ],
            options={
                'verbose_name': 'Журнал заявок',
                'verbose_name_plural': 'Журнал заявок',
            },
        ),
    ]