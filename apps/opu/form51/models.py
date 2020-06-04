from django.db import models
from django.urls import reverse

from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object


class Form51(models.Model):
    """Форма 5.1"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Примечание (№ID, МН, Аренда)")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="КО")
    num_ouss = models.CharField("Номер распоряжения ОУСС", max_length=250)
    order = models.ImageField('Распоряжение', upload_to='object/order/', blank=True)
    schema = models.ImageField('Схема', upload_to='object/schema/', blank=True)
    reserve = models.CharField('Резерва потока', max_length=15)
    reserve_object = models.ManyToManyField(Object, verbose_name="Трасса резерва потока", related_name="reserve_objects", blank=True, null=True)
    report_num = models.CharField('Номер донесения', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Форма 5.1'
        verbose_name_plural = 'Форма 5.1.'

    def __str__(self):
        return self.object.name