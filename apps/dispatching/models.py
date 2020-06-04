from django.db import models
from apps.accounts.models import Profile

from apps.accounts.models import DepartmentKT, SubdepartmentKT


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class TypeRequest(models.Model):
    '''Тип заявки (Например Квартирная заявка)'''
    name = models.CharField('Тип заявки', max_length=255)

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'

    def __str__(self):
        return self.name


class TypeOfApplicant(models.Model):
    ''' Вид заявки '''
    name = models.CharField('Вид заявителя', max_length=255)

    class Meta:
        verbose_name = 'Вид заявителя'
        verbose_name_plural = 'Виды заявителей'

    def __str__(self):
        return self.name


class Status(models.Model):
    ''' Статус заявки '''
    name = models.CharField('Статус', max_length=255)

    class Meta:
        verbose_name = 'Статус завки'
        verbose_name_plural = 'Статусы заявок'

    def __str__(self):
        return self.name


class Request(models.Model):
    '''Заявка'''
    type_request = models.ForeignKey(TypeRequest, verbose_name='Тип заявки', on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField('Адрес', max_length=355, blank=True, null=True)
    created_by = models.ForeignKey(Profile, verbose_name='Создан', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField('Имя заявителя', max_length=255, blank=True, null=True)
    last_name = models.CharField('Фамилия заявителя', max_length=255, blank=True, null=True)
    telephone_number = models.CharField('Номер телефона заявителя', max_length=50, blank=True, null=True)
    home_phone = models.CharField('Номер домашнего телефона', max_length=50, blank=True, null=True)
    description = models.CharField('Описание проблемы', max_length=500, blank=True, null=True)
    type_of_applicant = models.ForeignKey(TypeOfApplicant, verbose_name='Вид заявителя', on_delete=models.CASCADE, blank=True, null=True)
    date_from = models.DateTimeField(blank=True, null=True, verbose_name='От')
    date_to = models.DateTimeField(blank=True, null=True, verbose_name='До')
    department = models.ForeignKey(DepartmentKT, verbose_name='Отдел', on_delete=models.CASCADE, blank=True, null=True)
    subdepartment = models.ForeignKey(SubdepartmentKT, verbose_name='Подотдел',
                                      null=True, blank=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name='Статус заявка', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Журнал заявок'
        verbose_name_plural = 'Журнал заявок'

    def __str__(self):
        return self.description


class ShutdownType(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Вид отключения'
        verbose_name_plural = 'Виды отключений'

    def __str__(self):
        return self.name


class ShutdownLog(models.Model):
    """Журнал отключений"""
    shutdown_type = models.ForeignKey(ShutdownType, verbose_name='Вид отключения', on_delete=models.CASCADE)
    address = models.CharField('Адрес', max_length=355)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    сause = models.CharField('Причина', max_length=355)
    shutdown_periods_from = models.DateTimeField(verbose_name='Период отключения', blank=True, null=True)
    shutdown_periods_to = models.DateTimeField(verbose_name='Период отключения', blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Журнал отключений'
        verbose_name_plural = 'Журнал отключений'

    def __str__(self):
        return self.cause