# Generated by Django 2.2.4 on 2020-07-01 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('circuits', '0001_initial'),
        ('objects', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=255, verbose_name='Индекс')),
                ('name', models.CharField(max_length=255, verbose_name='Название индекса')),
            ],
            options={
                'verbose_name': 'Индекс события',
                'verbose_name_plural': 'Индекс события',
            },
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Причины',
                'verbose_name_plural': 'Причины',
            },
        ),
        migrations.CreateModel(
            name='TypeOfJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Виды журнала',
                'verbose_name_plural': 'Вид журнала',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateTimeField(blank=True, null=True, verbose_name='От')),
                ('date_to', models.DateTimeField(blank=True, null=True, verbose_name='До')),
                ('contact_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Передал (ФИО)')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('comments', models.CharField(blank=True, max_length=355, null=True, verbose_name='Комментарии')),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='circuits.Circuit', verbose_name='Каналы')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile', verbose_name='ФИО диспетчера')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer', verbose_name='Арендаторы')),
                ('index1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_index1', to='dispatching.Index', verbose_name='Индекс1')),
                ('index2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_index2', to='dispatching.Index', verbose_name='Индекс2')),
                ('ips', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.IP', verbose_name='ИП')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object', verbose_name='КО')),
                ('reason', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatching.Reason', verbose_name='Причины')),
                ('responsible_outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_outfit', to='objects.Outfit', verbose_name='Ответственный')),
                ('send_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_send_outfit', to='objects.Outfit', verbose_name='Передал (предприятие)')),
                ('type_journal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatching.TypeOfJournal', verbose_name='Вид журнала')),
            ],
            options={
                'verbose_name': 'Журнал событий',
                'verbose_name_plural': 'Журнал событий',
            },
        ),
    ]
