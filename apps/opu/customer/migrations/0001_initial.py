# Generated by Django 2.2.4 on 2021-08-17 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=250, verbose_name='Название')),
                ('abr', models.CharField(max_length=100, verbose_name='Абревиатура')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес')),
                ('email', models.CharField(blank=True, max_length=1250, null=True, verbose_name='Email и телефон')),
                ('diapozon', models.CharField(blank=True, max_length=1250, null=True, verbose_name='Диапозон нумераций')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('adding', models.CharField(blank=True, max_length=250, null=True, verbose_name='Примечание')),
            ],
            options={
                'verbose_name': 'Арендатор',
                'verbose_name_plural': 'Арендаторы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('customer', models.CharField(max_length=250, verbose_name='Название')),
                ('abr', models.CharField(max_length=100, verbose_name='Абревиатура')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес')),
                ('email', models.CharField(blank=True, max_length=1250, null=True, verbose_name='Email и телефон')),
                ('diapozon', models.CharField(blank=True, max_length=1250, null=True, verbose_name='Диапозон нумераций')),
                ('created_at', models.DateField(blank=True, editable=False, verbose_name='Дата')),
                ('adding', models.CharField(blank=True, max_length=250, null=True, verbose_name='Примечание')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_customer_log', to='customer.Customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Арендатор',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
