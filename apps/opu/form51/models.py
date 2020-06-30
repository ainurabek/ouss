from django.db import models
from django.urls import reverse

from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object

class Region(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регионы'
        verbose_name_plural = 'Регион'


class Image(models.Model):
    image = models.FileField(blank=False, null=False)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'



class Form51(models.Model):
    """Форма 5.1"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Примечание (№ID, МН, Аренда)", blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="КО", blank=True, null=True)
    num_ouss = models.CharField("Номер распоряжения ОУСС", max_length=250, blank=True, null=True)
    order = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    schema = models.ImageField('Схема', upload_to='object/schema/', blank=True, null=True)
    reserve = models.CharField('Резерва потока', max_length=15, blank=True, null=True)
    reserve_object = models.ManyToManyField(Object, verbose_name="Трасса резерва потока", related_name="reserve_objects", blank=True)
    report_num = models.CharField('Номер донесения', max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Форма 5.1'
        verbose_name_plural = 'Форма 5.1.'

    def __str__(self):
        return self.object.name