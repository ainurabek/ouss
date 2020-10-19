# Generated by Django 2.2.4 on 2020-10-19 16:42

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '__first__'),
        ('customer', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Режим',
                'verbose_name_plural': 'Режимы',
            },
        ),
        migrations.CreateModel(
            name='Speed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Скорость',
                'verbose_name_plural': 'Скорость',
            },
        ),
        migrations.CreateModel(
            name='TypeCom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип коммуникации',
                'verbose_name_plural': 'Типы коммуникации',
            },
        ),
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_circuit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер канала')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('type_using', models.CharField(blank=True, max_length=100, null=True)),
                ('num_order', models.CharField(blank=True, max_length=100, null=True)),
                ('date_order', models.CharField(blank=True, max_length=100, null=True)),
                ('num_arenda', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер')),
                ('speed', models.CharField(blank=True, max_length=100, null=True)),
                ('adding', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
                ('comments', models.CharField(blank=True, max_length=100, null=True)),
                ('first', models.BooleanField(default=False, verbose_name='Используется/Не используется')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_cat', to='objects.Category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_cust', to='customer.Customer')),
                ('final_destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_final_dest', to='objects.Point')),
                ('id_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_obj', to='objects.Object')),
                ('id_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='circuits.Circuit')),
                ('in_out', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_in', to='objects.InOut')),
                ('measure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_measure', to='circuits.Measure')),
                ('mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_mode', to='circuits.Mode')),
                ('point1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_ip1', to='objects.Point')),
                ('point2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_ip2', to='objects.Point')),
                ('transit', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='cir_transit_obj1', to='circuits.Circuit')),
                ('transit2', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='cir_transit_obj2', to='circuits.Circuit')),
                ('type_com', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circ_type_com', to='circuits.TypeCom')),
            ],
            options={
                'verbose_name': 'Канал для Формы 5.3',
                'verbose_name_plural': 'Каналы для Формы 5.3',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Bypass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=100, null=True)),
                ('num_p', models.CharField(blank=True, max_length=100, null=True)),
                ('id_bypass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_bypass', to='circuits.Circuit')),
                ('id_main', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bypass_id_main', to='circuits.Circuit')),
            ],
        ),
        migrations.CreateModel(
            name='AssignPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_object_main', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_obj_main', to='objects.Object')),
                ('id_object_part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_obj_part', to='objects.Object')),
            ],
        ),
    ]
