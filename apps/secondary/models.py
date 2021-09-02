from django.db import models
from apps.accounts.models import Profile
from apps.opu.objects.models import Outfit, Point
from django.contrib.auth import get_user_model


User = get_user_model()

class TypeStation(models.Model):
    name = models.CharField("Название", max_length=150)

    class Meta:
        verbose_name = "Тип станции"
        verbose_name_plural = "Тип станции"

    def __str__(self):
        return self.name

class SecondaryBase(models.Model):
    '''База вторичной сети Для СВС'''
    point = models.ForeignKey(Point, verbose_name="ИП", on_delete=models.SET_NULL, related_name="point_secondary", null=True, blank=True)
    outfit = models.ForeignKey(Outfit, related_name='second_out', on_delete=models.SET_NULL, blank=True, null=True)
    type_station = models.ForeignKey(TypeStation, related_name='type_station_second', on_delete=models.SET_NULL, blank=True, null=True)
    year_of_launch = models.CharField('Год запуска', max_length=500, null=True, blank=True)
    installed_value = models.CharField('Монтированная емкость', max_length=1500, blank=True, null=True)
    active_value = models.CharField('Задействованная емкость', max_length=1500, blank=True, null=True)
    active_numbering = models.CharField('Задействованная нумерация', max_length=1500, null=True, blank=True)
    free_numbering = models.CharField('Свободная нумерация', max_length=2500, blank=True, null=True)
    GAS_numbering = models.CharField('Выделенная ГАС нумерация', max_length=2500, null=True, blank=True)
    GAS_return = models.CharField('Возврат в ГАС', max_length=2500, null=True, blank=True)
    KT_numbering = models.IntegerField('Нумерация КТ', default=0, null=True, blank=True)
    comments = models.CharField('Примечание', max_length=1500, null=True, blank=True)
    created_by = models.ForeignKey(Profile, verbose_name='ФИО диспетчера', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField('Дата создания', blank=True, null=True)
    administrative_division = models.CharField('Примечание', max_length=2500, null=True, blank=True)
    zone_code = models.CharField('Зон код АВ', max_length=2500, null=True, blank=True)
    inner_zone_code = models.CharField('Внутризон. Код АВ', max_length=2500, null=True, blank=True)
    amount_of_numbers = models.IntegerField("Количество выделенных номеров", default=0, blank=True, null=True)


    class Meta:
        verbose_name = 'База вторичной сети'
        verbose_name_plural = 'База вторичной сети'
        ordering = ('id',)
        get_latest_by = ('id')

class AmbulanceNumsBase(models.Model):
    '''База вторичной сети Для 118'''
    outfit = models.ForeignKey(Outfit, related_name='ambul_out', on_delete=models.SET_NULL, blank=True, null=True)
    region = models.CharField('Район', max_length=500, null=True, blank=True)
    code = models.CharField('Код',  max_length=500, blank=True, null=True)
    main_num = models.CharField('Главный номер', max_length=1500, blank=True, null=True)
    first_redirection= models.CharField('Первая переадресация', max_length=5500, null=True, blank=True)
    second_redirection = models.CharField('Вторая переадресация', max_length=5500, blank=True, null=True)
    third_redirection = models.CharField('Третья переадресация', max_length=5500, null=True, blank=True)
    comments = models.CharField('Примечание', max_length=1500, null=True, blank=True)
    created_by = models.ForeignKey(Profile, verbose_name='ФИО диспетчера', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField('Дата создания', blank=True, null=True)

    class Meta:
        verbose_name = 'База тел.номеров 118'
        verbose_name_plural = 'База тел.номеров 118'
        ordering = ('id',)
        get_latest_by = ('id')


