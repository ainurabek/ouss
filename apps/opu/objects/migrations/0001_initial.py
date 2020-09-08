# Generated by Django 2.2.4 on 2020-09-08 14:32

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=100, verbose_name='Индекс')),
                ('name', models.CharField(max_length=100, verbose_name='Обозначение')),
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
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='LineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип линии',
                'verbose_name_plural': 'Типы линии',
            },
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outfit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Аббревиатура')),
                ('adding', models.CharField(max_length=100, verbose_name='Название')),
                ('num_outfit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
            },
        ),
        migrations.CreateModel(
            name='TPO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'invalid': 'Это поле обязательно.'}, max_length=100, verbose_name='Название')),
                ('index', models.CharField(max_length=100, verbose_name='Индекс')),
            ],
            options={
                'verbose_name': 'ТПО',
                'verbose_name_plural': 'ТПО',
            },
        ),
        migrations.CreateModel(
            name='TypeOfLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
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
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'ПГ/ВГ/ТГ/ЧГ/РГ',
                'verbose_name_plural': 'ПГ/ВГ/ТГ/ЧГ/РГ',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=100, verbose_name='ИП')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('id_outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point_out', to='objects.Outfit')),
                ('tpo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point_tpo', to='objects.TPO')),
            ],
        ),
        migrations.CreateModel(
            name='OutfitWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('outfit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outfit_worker', to='objects.Outfit')),
            ],
            options={
                'verbose_name': 'Сотрудник предприятия',
                'verbose_name_plural': 'Сотрудники предприятий',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='outfit',
            name='tpo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.TPO'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='type_outfit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.TypeOfLocation'),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('inter_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Международное обозначение')),
                ('trakt', models.BooleanField(blank=True, null=True, verbose_name='Тракт/Линия')),
                ('num', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер задейственного канала')),
                ('comments', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
                ('amount_channels', models.CharField(blank=True, max_length=100, null=True, verbose_name='Количество каналов')),
                ('save_in', models.BooleanField(blank=True, null=True, verbose_name='Сохранить')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('add_time', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_category', to='objects.Category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Profile')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obj_cust', to='customer.Customer')),
                ('id_outfit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_out', to='objects.Outfit')),
                ('id_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='objects.Object')),
                ('our', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_our', to='objects.TypeOfLocation')),
                ('point1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_point', to='objects.Point', verbose_name='ИП приема')),
                ('point2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_point2', to='objects.Point', verbose_name='ИП пер')),
                ('tpo1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_tpo', to='objects.TPO')),
                ('tpo2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_tpo2', to='objects.TPO')),
                ('transit', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='transit_obj1', to='objects.Object')),
                ('transit2', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='transit_obj2', to='objects.Object')),
                ('type_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_type_line', to='objects.LineType')),
                ('type_of_trakt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_trakt_type', to='objects.TypeOfTrakt')),
            ],
            options={
                'verbose_name': 'Линия передачи/Обьект/Тракт',
                'verbose_name_plural': 'Линия передачи/Обьект/Тракт',
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_object', to='objects.Object')),
                ('point_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_point', to='objects.Point')),
                ('tpo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='objects.TPO')),
            ],
            options={
                'verbose_name': 'ИП',
                'verbose_name_plural': 'ИП',
            },
        ),
    ]
