# Generated by Django 2.2.4 on 2021-08-17 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_description', models.CharField(max_length=205)),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Список действий',
                'verbose_name_plural': 'Список действий',
            },
        ),
    ]
