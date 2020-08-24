# Generated by Django 2.2.4 on 2020-08-21 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_profile_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subdepartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_subdepartment', to='accounts.SubdepartmentKT', verbose_name='Подотдел пользователя'),
        ),
    ]