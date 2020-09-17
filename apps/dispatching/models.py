from django.db import models
from apps.accounts.models import Profile

from apps.accounts.models import DepartmentKT, SubdepartmentKT

from apps.opu.circuits.models import Circuit
from apps.opu.customer.models import Customer

from apps.opu.objects.models import Outfit, Object, IP, Point

from apps.opu.objects.models import Outfit, Object, IP, OutfitWorker




class TypeOfJournal(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виды журнала'
        verbose_name_plural = 'Вид журнала'


class Reason(models.Model):
    name = models.CharField(max_length=150)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Причины'
        verbose_name_plural = 'Причины'

class Comments(models.Model):
    name = models.CharField(max_length=150)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Примечание'
        verbose_name_plural = 'Примечание'

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
    id_parent = models.ForeignKey('Event', related_name='event_id_parent', on_delete=models.CASCADE, null=True, blank=True)
    type_journal = models.ForeignKey(TypeOfJournal, verbose_name='Вид журнала', on_delete=models.CASCADE)
    date_from = models.DateTimeField(blank=True, null=True, verbose_name='От')
    date_to = models.DateTimeField(blank=True, null=True, verbose_name='До')
    date_calls = models.DateTimeField(blank=True, null=True, verbose_name='Время звонка')
    created_by = models.ForeignKey(Profile, verbose_name='ФИО диспетчера', on_delete=models.SET_NULL, null=True, blank=True)
    contact_name = models.ForeignKey(OutfitWorker, verbose_name='Передал (ФИО)', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField('Дата создания', blank=True, null=True)
    reason = models.ForeignKey(Reason, verbose_name='Причины', on_delete=models.SET_NULL, null=True, blank=True)
    index1 = models.ForeignKey(Index, related_name='event_index1', verbose_name='Индекс1', on_delete=models.CASCADE, null=True,
                                          blank=True)
    comments1 = models.CharField('Примечание1', max_length=500, null=True, blank=True)

    responsible_outfit = models.ForeignKey(Outfit, verbose_name='Ответственный', on_delete=models.SET_NULL,
                                          null=True, blank=True,  related_name='dispatch_outfit')
    send_from = models.ForeignKey(Outfit, verbose_name='Передал (предприятие)', on_delete=models.SET_NULL,
                                          null=True, blank=True,  related_name='dispatch_send_outfit')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='event_obj', verbose_name="КО",  null=True, blank=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='event_cir', verbose_name="Каналы", null=True, blank=True)
    ips = models.ForeignKey(IP, on_delete=models.CASCADE, verbose_name="ИПы", related_name='event_ips', null=True, blank=True)
    customer = models.ForeignKey(Customer, verbose_name="Арендаторы", on_delete=models.CASCADE, null=True, blank=True)
    point1 = models.ForeignKey(Point, verbose_name="Ип от", on_delete=models.SET_NULL, related_name="point1_event", null=True, blank=True)
    point2 = models.ForeignKey(Point, verbose_name="Ип до", on_delete=models.SET_NULL, related_name="point2_event", null=True, blank=True)
    name = models.CharField('Название', max_length=500, null=True, blank=True)
    callsorevent = models.BooleanField(default=True)
    period_of_time = models.CharField("Сумма часов, за которое устранили аварию", max_length=100, blank=True, null=True)
    previous = models.OneToOneField("Event", related_name="event_previous", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Журнал событий'
        verbose_name_plural = 'Журнал событий'
        ordering = ('id',)
        get_latest_by = ('id')

    def __str__(self):
        return str(self.id)



