# Generated by Django 2.2.4 on 2020-10-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Bypass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=100, null=True)),
                ('num_p', models.CharField(blank=True, max_length=100, null=True)),
            ],
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
            ],
            options={
                'verbose_name': 'Канал для Формы 5.3',
                'verbose_name_plural': 'Каналы для Формы 5.3',
                'ordering': ('id',),
            },
        ),
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
    ]
