# Generated by Django 2.2.4 on 2020-03-04 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='InOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'ИП',
                'verbose_name_plural': 'ИП',
            },
        ),
        migrations.CreateModel(
            name='LineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип линии',
                'verbose_name_plural': 'Типы линии',
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('COreceive', models.CharField(blank=True, max_length=100, null=True, verbose_name='КО прием')),
                ('COdeliver', models.CharField(blank=True, max_length=100, null=True, verbose_name='КО передачи')),
                ('inter_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Международное обозначение')),
                ('trakt', models.BooleanField(blank=True, null=True)),
                ('num', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер задейственного канала')),
                ('main', models.BooleanField()),
                ('_complex', models.BooleanField()),
                ('type_transit1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тип транзита1')),
                ('type_transit2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тип транзита2')),
                ('comments', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
                ('handel_add_path1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Начало')),
                ('handel_add_path2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Конец')),
                ('amount_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество каналов')),
                ('not_in_use', models.BooleanField(verbose_name='Активный/Нет')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_category', to='objects.Category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_cust', to='customer.Customer')),
                ('destination1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_dest1', to='objects.IP')),
                ('destination2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_dest2', to='objects.IP')),
            ],
            options={
                'verbose_name': 'Линия передачи/Обьект/Тракт',
                'verbose_name_plural': 'Линия передачи/Обьект/Тракт',
            },
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outfit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Аббревиатура')),
                ('adding', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('num_outfit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Вид системы',
                'verbose_name_plural': 'Вид системы',
            },
        ),
        migrations.CreateModel(
            name='TPO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('tpo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
            ],
            options={
                'verbose_name': 'ТПО',
                'verbose_name_plural': 'ТПО',
            },
        ),
        migrations.CreateModel(
            name='TraktOrLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Линия/Тракт',
                'verbose_name_plural': 'Линия/Тракт',
            },
        ),
        migrations.CreateModel(
            name='TypeOfLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип принадлежности',
                'verbose_name_plural': 'Тип принадлежности',
            },
        ),
        migrations.CreateModel(
            name='TypeOfTrakt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(blank=True, max_length=100, null=True, verbose_name='Индекс')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('group', models.CharField(blank=True, max_length=100, null=True, verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Тип тракта',
                'verbose_name_plural': 'Тип тракта',
            },
        ),
        migrations.CreateModel(
            name='Trassa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Трасса',
                'verbose_name_plural': 'Трасса',
            },
        ),
        migrations.CreateModel(
            name='TransitObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('id_complex_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_complex_obj', to='objects.Object')),
                ('id_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='id_transit_obj', to='objects.Object')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(blank=True, max_length=100, null=True, verbose_name='ИП')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название')),
                ('id_outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point_out', to='objects.Outfit')),
                ('tpo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point_tpo', to='objects.TPO')),
            ],
        ),
        migrations.AddField(
            model_name='outfit',
            name='tpo',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='objects.TPO'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='type_outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_tpo', to='objects.TypeOfLocation'),
        ),
        migrations.AddField(
            model_name='object',
            name='id_outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_out', to='objects.Outfit'),
        ),
        migrations.AddField(
            model_name='object',
            name='id_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object'),
        ),
        migrations.AddField(
            model_name='object',
            name='id_transit1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transit_obj', to='objects.Object'),
        ),
        migrations.AddField(
            model_name='object',
            name='id_transit2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transit2_obj', to='objects.Object'),
        ),
        migrations.AddField(
            model_name='object',
            name='our',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_our', to='objects.TypeOfLocation'),
        ),
        migrations.AddField(
            model_name='object',
            name='point1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_point', to='objects.Point', verbose_name='ИП приема'),
        ),
        migrations.AddField(
            model_name='object',
            name='point2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_point2', to='objects.Point', verbose_name='ИП пер'),
        ),
        migrations.AddField(
            model_name='object',
            name='system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_system', to='objects.System'),
        ),
        migrations.AddField(
            model_name='object',
            name='tpo1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_tpo', to='objects.TPO'),
        ),
        migrations.AddField(
            model_name='object',
            name='tpo2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_tpo2', to='objects.TPO'),
        ),
        migrations.AddField(
            model_name='object',
            name='trassa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object_trasa', to='objects.Trassa'),
        ),
        migrations.AddField(
            model_name='object',
            name='type_line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_type_line', to='objects.LineType'),
        ),
        migrations.AddField(
            model_name='object',
            name='type_of_trakt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_trakt_type', to='objects.TypeOfTrakt'),
        ),
        migrations.AddField(
            model_name='ip',
            name='object_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object'),
        ),
        migrations.AddField(
            model_name='ip',
            name='point_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Point'),
        ),
        migrations.AddField(
            model_name='ip',
            name='tpo_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.TPO'),
        ),
    ]
