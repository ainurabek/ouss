

from apps.opu.circuits.models import Circuit
from django.db import models
from apps.accounts.models import Profile
from simple_history.models import HistoricalRecords



class Form53(models.Model):
    """Форма 5.3"""
    circuit = models.OneToOneField(Circuit, on_delete=models.CASCADE, verbose_name="Каналы", blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(related_name='history_form53_log')

    class Meta:
        verbose_name = 'Форма 5.3'
        verbose_name_plural = 'Форма 5.3.'
        ordering = ('id',)

    def __str__(self):
        return self.circuit.name

class Schema53Photo(models.Model):
    src = models.ImageField('Схема', upload_to='object/schema/', blank=True, null=True)
    form53 = models.ManyToManyField(Form53, verbose_name="Схема",
                                 blank=True, related_name="schema53_photo")


class Order53Photo(models.Model):
    src = models.ImageField('Схема', upload_to='object/order/', blank=True)
    form53 = models.ManyToManyField(Form53, verbose_name="Распоряжение",
                                 blank=True, related_name="order53_photo")