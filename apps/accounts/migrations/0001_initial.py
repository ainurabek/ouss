# Generated by Django 2.2.4 on 2020-09-08 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_profile_created', models.BooleanField(default=False, verbose_name='Создан ли профиль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='DepartmentKT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'роль',
                'verbose_name_plural': 'пользовательские роли',
            },
        ),
        migrations.CreateModel(
            name='SubdepartmentKT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Подотдел')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supdepartment', to='accounts.DepartmentKT', verbose_name='Подотдел')),
            ],
            options={
                'verbose_name': 'Подотдел',
                'verbose_name_plural': 'Подотделы',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=30, null=True, verbose_name='Должность')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Отчество')),
                ('online', models.BooleanField(default=False, verbose_name='В Сети')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Муж'), ('F', 'Жен')], max_length=10, null=True, verbose_name='Пол')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Рабочий номер телефона')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_profile', to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Журнал входа',
                'verbose_name_plural': 'Журнал входа',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_department', to='accounts.DepartmentKT', verbose_name='Отдел пользователя'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_role', to='accounts.Role', verbose_name='Роль пользователя'),
        ),
        migrations.AddField(
            model_name='user',
            name='subdepartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_subdepartment', to='accounts.SubdepartmentKT', verbose_name='Подотдел пользователя'),
        ),
    ]
