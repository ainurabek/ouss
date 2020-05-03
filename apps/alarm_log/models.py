from django.db import models
from apps.accounts.models import Profile
from apps.form51.models import Region


class TypeStatement(models.Model):
    '''Тип заявки (Например Квартирная заявка)'''
    name = models.CharField('Тип заявки', max_length=255)

    class Meta:
        verbose_name = 'Тип заявка'
        verbose_name_plural = 'Типы заявок'

    def __str__(self):
        return self.name


class TypeOfStatement(models.Model):
    ''' Вид заявки '''
    name = models.CharField('Вид заявки', max_length=255)

    class Meta:
        verbose_name = 'Вид заявка'
        verbose_name_plural = 'Виды заявок'

    def __str__(self):
        return self.name


class Status(models.Model):
    ''' Статус заявки '''
    name = models.CharField('Статус', max_length=255)

    class Meta:
        verbose_name = 'Статус завка'
        verbose_name_plural = 'Статусы заявок'

    def __str__(self):
        return self.name


class Departament(models.Model):
    '''Отделы'''
    name = models.CharField('Название отдела', max_length=255)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Statement(models.Model):
    '''Заявка'''
    type_statement = models.ForeignKey(TypeStatement, verbose_name='Тип заявки', on_delete=models.CASCADE)
    address = models.CharField('Адрес', max_length=355)
    created_by = models.ForeignKey(Profile, verbose_name='Контактное лицо', on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    telephone_number = models.CharField('Номер телефона', max_length=50, blank=True, null=True)
    home_phone = models.CharField('Номер домашнего телефона', max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    type_of_statement = models.ForeignKey(TypeOfStatement, verbose_name='Вид заявки', on_delete=models.CASCADE)
    date_from = models.DateTimeField(blank=True, null=True, verbose_name='От')
    date_to = models.DateTimeField(blank=True, null=True, verbose_name='До')
    specialist = models.ForeignKey(Departament, verbose_name='Отдел', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name='Статус заявка', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

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