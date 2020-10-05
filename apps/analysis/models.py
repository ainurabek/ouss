from django.db import models

from apps.opu.objects.models import Outfit

from apps.dispatching.models import Event


class FormAK(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name = "formak_outfit", null=True, blank=True)
    punkt5_total_outfit_kls = models.IntegerField('Продолжительность всех ПВ кан*час(КЛС)', null=True, blank=True)
    punkt5_total_outfit_rrl = models.IntegerField('Продолжительность всех ПВ кан*час(РРЛ)', null=True, blank=True)


    class Meta:
        verbose_name = 'Форма АК'
        verbose_name_plural = 'Форма АК'

    def __str__(self):
        return str(self.id)

class Punkt5(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name = "punkt5_outfit", null=True, blank=True)
    form_ak = models.ForeignKey(FormAK, on_delete=models.CASCADE, related_name = "punkt5_form", null=True, blank=True)
    name = models.CharField('Название', max_length=500, null=True, blank=True)
    country_punkt5_total = models.CharField('Республика', max_length=500, null=True, blank=True)
    punkt5_total_outfit_kls = models.IntegerField('Продолжительность всех ПВ кан*час(КЛС)', null=True, blank=True)
    punkt5_total_outfit_rrl = models.IntegerField('Продолжительность всех ПВ кан*час(РРЛ)', null=True, blank=True)
    total_outfit_region_kls = models.IntegerField('Протяженность кан*км зад.(КЛС)', null=True, blank=True)
    total_outfit_region_rrl = models.IntegerField('Протяженность кан*км зад.(РРЛ)', null=True, blank=True)
    stops_kls = models.IntegerField('Простои на 1000 кан*км (КЛС)', null=True, blank=True)
    stops_rrl = models.IntegerField('Простои на 1000 кан*км (РРЛ)', null=True, blank=True)
    coefficient_kls = models.IntegerField('Коэффициент качества (КЛС)', null=True, blank=True)
    coefficient_rrl = models.IntegerField('Коэффициент качества (РРЛ)', null=True, blank=True)
    total_punkt5 = models.IntegerField('Общая протяж.кан*км', null=True, blank=True)
    KLS = models.IntegerField('КЛС', null=True, blank=True)
    RRL = models.IntegerField('РРЛ', null=True, blank=True)
    total_coefficient = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Пункт №5'
        verbose_name_plural = 'Пункт №5'

    def __str__(self):
        return str(self.id)