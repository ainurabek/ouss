from django.db import models
from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object
from apps.opu.circuits.models import Circuit
from simple_history.models import HistoricalRecords

class Signalization(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Сигнализация'
        verbose_name_plural = 'Сигнализация'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Form_Customer(models.Model):
    """Форма для арендаторов"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    object = models.OneToOneField(Object, on_delete=models.CASCADE, verbose_name="КО", blank=True, null=True)
    circuit = models.OneToOneField(Circuit, on_delete=models.CASCADE, verbose_name="Каналы", blank=True, null=True)
    amount_flow = models.CharField('Количество потоков', max_length=200, blank=True, null=True)
    signalization = models.ForeignKey(Signalization, related_name='cust_sign', on_delete=models.SET_NULL, blank=True,
                                      null=True)
    type_of_using = models.CharField('Вид использования', max_length=200, blank=True, null=True)
    num_order = models.CharField("Номер распоряжения", max_length=250, blank=True, null=True)
    comments = models.CharField("Примечание", max_length=250, blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(related_name='history_form_customer_log')

    class Meta:
        verbose_name = 'Форма для Арендаторов'
        verbose_name_plural = 'Форма для Арендаторов'
        ordering = ('id',)

    def __str__(self):
        return self.customer.abr


class OrderCusPhoto(models.Model):
    src = models.FileField('Схема', upload_to='files/', blank=True, null=True)
    form_customer = models.ForeignKey(Form_Customer, on_delete=models.CASCADE, verbose_name="Распоряжение",
                                 blank=True, null=True, related_name="order_cust_photo")