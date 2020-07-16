from django.db import models
from django.urls import reverse

from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object
from apps.opu.circuits.models import Circuit


from django.db import models
from django.urls import reverse

from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object


class Form53(models.Model):
    """Форма 5.3"""
    circuit = models.OneToOneField(Circuit, on_delete=models.CASCADE, verbose_name="Каналы", blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Форма 5.3'
        verbose_name_plural = 'Форма 5.3.'

    def __str__(self):
        return self.circuit.name


class Schema53Photo(models.Model):
    schema = models.ImageField('Схема', upload_to='object/schema/', blank=True, null=True)
    form51 = models.ForeignKey(Form53, on_delete=models.CASCADE, verbose_name="Схема",
                                 blank=True, null=True, related_name="schema53_photo")


class Order53Photo(models.Model):
    order = models.ImageField('Схема', upload_to='object/order/', blank=True, null=True)
    form51 = models.ForeignKey(Form53, on_delete=models.CASCADE, verbose_name="Распоряжение",
                                 blank=True, null=True, related_name="order53_photo")