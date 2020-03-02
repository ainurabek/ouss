# Generated by Django 2.2.4 on 2020-03-02 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('objects', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
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
                ('index', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Скорость',
                'verbose_name_plural': 'Скорость',
            },
        ),
        migrations.CreateModel(
            name='SubsRoutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(blank=True, max_length=100, null=True)),
                ('route', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
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
                ('id_circuit', models.CharField(blank=True, max_length=100, null=True)),
                ('num_circuit', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type_using', models.CharField(blank=True, max_length=100, null=True)),
                ('num_order', models.CharField(blank=True, max_length=100, null=True)),
                ('date_order', models.CharField(blank=True, max_length=100, null=True)),
                ('num_arenda', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер телефона')),
                ('adding', models.CharField(blank=True, max_length=100, null=True)),
                ('comments', models.CharField(blank=True, max_length=100, null=True)),
                ('type_transit1', models.CharField(blank=True, max_length=100, null=True)),
                ('type_transit2', models.CharField(blank=True, max_length=100, null=True)),
                ('id_transit1', models.CharField(blank=True, max_length=100, null=True)),
                ('id_transit2', models.CharField(blank=True, max_length=100, null=True)),
                ('first', models.BooleanField()),
                ('handel_add_path1', models.CharField(blank=True, max_length=100, null=True)),
                ('handel_add_path2', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_category', to='objects.Category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_cust', to='customer.Customer')),
                ('destination1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_ip1', to='objects.IP')),
                ('destination2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_ip2', to='objects.IP')),
                ('id_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_obj', to='objects.Object')),
                ('id_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='circuits.Circuit')),
                ('id_subst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_subst', to='circuits.SubsRoutes')),
                ('in_out', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_in', to='objects.InOut')),
                ('measure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_measure', to='circuits.Measure')),
                ('mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_mode', to='circuits.Mode')),
                ('speed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_speed', to='circuits.Speed')),
                ('type_com', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='circ_type_com', to='circuits.Type')),
            ],
            options={
                'verbose_name': 'Канал',
                'verbose_name_plural': 'Каналы',
            },
        ),
        migrations.CreateModel(
            name='Bypass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(blank=True, max_length=100, null=True)),
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
                ('_id', models.CharField(blank=True, max_length=100, null=True)),
                ('id_object_main', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_obj_main', to='objects.Object')),
                ('id_object_part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_obj_part', to='objects.Object')),
            ],
        ),
    ]
