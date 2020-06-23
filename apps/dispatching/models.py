from django.db import models
from apps.accounts.models import Profile

from apps.accounts.models import DepartmentKT, SubdepartmentKT

from apps.opu.circuits.models import Circuit
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Outfit, Object, IP



class TypeOfJournal(models.Model):
    name = models.CharField(max_length=150)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виды журнала'
        verbose_name_plural = 'Вид журнала'

class Choice(models.Model):
    '''Тип заявки (Например Квартирная заявка)'''
    index = models.CharField('Индекс', max_length=255)
    name = models.CharField('Название выбора', max_length=255)

    class Meta:
        verbose_name = 'Выбор по'
        verbose_name_plural = 'Выбор по'

    def __str__(self):
        return self.name

class Reason(models.Model):
    name = models.CharField(max_length=150)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Причины'
        verbose_name_plural = 'Причины'

class Index(models.Model):
    '''Тип заявки (Например Квартирная заявка)'''
    index = models.CharField('Индекс', max_length=255)
    name = models.CharField('Название индекса', max_length=255)

    class Meta:
        verbose_name = 'Индекс события'
        verbose_name_plural = 'Индекс события'

    def __str__(self):
        return self.index



class Event(models.Model):
    '''Событие'''
    type_journal = models.ForeignKey(TypeOfJournal, verbose_name='Вид журнала', on_delete=models.CASCADE, blank=True, null=True)
    date_from = models.DateTimeField(blank=True, null=True, verbose_name='От')
    date_to = models.DateTimeField(blank=True, null=True, verbose_name='До')
    created_by = models.ForeignKey(Profile, verbose_name='ФИО диспетчера', on_delete=models.CASCADE, blank=True, null=True)
    contact_name = models.CharField('Передал (ФИО)', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    reason = models.ForeignKey(Reason, verbose_name='Причины', on_delete=models.CASCADE, blank=True, null=True)
    index= models.ForeignKey(Index, verbose_name='Индекс', on_delete=models.CASCADE,
                                          blank=True, null=True)
    comments = models.CharField('Комментарии', max_length=355, blank=True, null=True)
    responsible_outfit = models.ForeignKey(Outfit, verbose_name='Ответственный', on_delete=models.CASCADE,
                                          blank=True, null=True, related_name='dispatch_outfit')
    send_from = models.ForeignKey(Outfit, verbose_name='Передал (предприятие)', on_delete=models.CASCADE,
                                          blank=True, null=True, related_name='dispatch_send_outfit')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="КО", blank=True, null=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, verbose_name="Каналы", blank=True, null=True)
    ips = models.ForeignKey(IP, on_delete=models.CASCADE, verbose_name="ИП", blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name="Арендаторы", on_delete=models.CASCADE, blank=True, null=True)
    choice = models.ForeignKey(Choice, verbose_name="выбор по", on_delete=models.CASCADE, blank=True, null=True)



    class Meta:
        verbose_name = 'Журнал событий'
        verbose_name_plural = 'Журнал событий'

    def __str__(self):
        return self.type_journal.name


