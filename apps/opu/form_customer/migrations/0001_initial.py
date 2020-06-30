# Generated by Django 2.2.4 on 2020-06-30 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('circuits', '0001_initial'),
        ('objects', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Сигнализация',
                'verbose_name_plural': 'Сигнализация',
            },
        ),
        migrations.CreateModel(
            name='Form_Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_flow', models.CharField(blank=True, max_length=200, null=True, verbose_name='Количество потоков')),
                ('type_of_using', models.CharField(blank=True, max_length=200, null=True, verbose_name='Вид использования')),
                ('num_order', models.CharField(blank=True, max_length=250, null=True, verbose_name='Номер распоряжения')),
                ('order', models.ImageField(blank=True, null=True, upload_to='object/order/', verbose_name='Распоряжение')),
                ('comments', models.CharField(blank=True, max_length=250, null=True, verbose_name='Примечание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='circuits.Circuit', verbose_name='Каналы')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object', verbose_name='КО')),
                ('signalization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cust_sign', to='form_customer.Signalization')),
            ],
            options={
                'verbose_name': 'Форма для Арендаторов',
                'verbose_name_plural': 'Форма для Арендаторов',
            },
        ),
    ]
