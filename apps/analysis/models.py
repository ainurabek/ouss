from django.db import models
from apps.accounts.models import Profile
from apps.opu.objects.models import Outfit, MainLineType

from apps.opu.objects.models import Object, Point


class FormAnalysis(models.Model):
    id_parent = models.ForeignKey("FormAnalysis", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Название", max_length=255, blank=True, null=True)
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия")
    average_coefficient = models.FloatField("Средний коэффициент качества", default=0, blank=True, null=True)
    coefficient = models.FloatField("Коэффициент качества", default=0, blank=True, null=True)

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Средний Кеффициент"
        verbose_name_plural = "Средний Кеффициент"

class AmountChannelsKLSRRL(models.Model):
    object = models.OneToOneField(Object, related_name = 'object_channelKLSRRL', on_delete=models.CASCADE, blank=True, null=True)
    ips = models.OneToOneField(Point, related_name = 'point_channelKLSRRL', on_delete=models.CASCADE, blank=True, null=True)
    amount_channelsKLS = models.IntegerField("КЛС каналы", default=0, blank=True, null=True)
    amount_channelsRRL = models.IntegerField("ЦРРЛ каналы", default=0,  blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Количество каналов (КЛС и ЦЦРЛ)"
        verbose_name_plural = "Количество каналов (КЛС и ЦЦРЛ)"


class Punkt5(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия")
    form_analysis = models.OneToOneField(FormAnalysis, on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Форма анализа", related_name="punkt5")

    outfit_period_of_time_kls = models.FloatField("Продолжительность всех ПВ кан*час КЛС", blank=True, null=True, default=0)
    downtime_kls = models.FloatField("Простои КЛС", default=0, blank=True, null=True)
    coefficient_kls = models.IntegerField("Коэффициент качества КЛС", default=0, blank=True, null=True)

    outfit_period_of_time_vls = models.FloatField("Продолжительность всех ПВ кан*час ВЛС", blank=True, null=True, default=0)
    downtime_vls = models.FloatField("Простои ВЛС", default=0, blank=True, null=True)
    coefficient_vls = models.IntegerField("Коэффициент качества ВЛС", default=0, blank=True, null=True)

    outfit_period_of_time_rrl = models.FloatField("Продолжительность всех ПВ кан*час РРЛ", blank=True, null=True, default=0)
    downtime_rrl = models.FloatField("Простои РРЛ", default=0, blank=True, null=True)
    coefficient_rrl = models.IntegerField("Коэффициент качества РРЛ", default=0, blank=True, null=True)

    formula_activate = models.BooleanField(default=True)
    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "п.5"
        verbose_name_plural = "п.5"

    def __str__(self):
        return f"{self.id}"


class Punkt7(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия")
    form_analysis = models.OneToOneField(FormAnalysis, on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Форма анализа", related_name="punkt7")

    total_number_kls = models.IntegerField("Общее количество линейных трактов КЛС", default=0, blank=True, null=True)
    corresponding_norm_kls = models.IntegerField("Соответствующих норме КЛС", default=0, blank=True, null=True)
    percentage_compliance_kls = models.IntegerField("Процент соответствия КЛС", default=0, blank=True, null=True)
    coefficient_kls = models.IntegerField("Коэффициент качества КЛС", default=0, blank=True, null=True)

    total_number_vls = models.IntegerField("Общее количество линейных трактов ВЛС", default=0, blank=True, null=True)
    corresponding_norm_vls = models.IntegerField("Соответствующих норме ВЛС", default=0, blank=True, null=True)
    percentage_compliance_vls = models.IntegerField("Процент соответствия ВЛС", default=0, blank=True, null=True)
    coefficient_vls = models.IntegerField("Коэффициент качества", default=0, blank=True, null=True)

    total_number_rrl = models.IntegerField("Общее количество линейных трактов РРЛ", default=0, blank=True, null=True)
    corresponding_norm_rrl = models.IntegerField("Соответствующих норме РРЛ", default=0, blank=True, null=True)
    percentage_compliance_rrl = models.IntegerField("Процент соответствия РРЛ", default=0, blank=True, null=True)
    coefficient_rrl = models.IntegerField("Коэффициент качества РРЛ", default=0, blank=True, null=True)

    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "п.7"
        verbose_name_plural = "п.7"

    def __str__(self):
        return f"{self.id}"


class TotalData(models.Model):
    total_length = models.FloatField("Общая протяж. кан*км", default=0, blank=True, null=True)
    total_coefficient = models.FloatField("Коэффициент качества", default=0, blank=True, null=True)

    punkt5 = models.OneToOneField(Punkt5, related_name="total_data5", on_delete=models.CASCADE, blank=True, null=True)
    punkt7 = models.OneToOneField(Punkt7, related_name="total_data7", on_delete=models.CASCADE, blank=True, null=True)

    kls = models.FloatField("Значение", default=0, blank=True, null=True)
    vls = models.FloatField("Значение", default=0, blank=True, null=True)
    rrl = models.FloatField("Значение", default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Удельный вес протяженности"
        verbose_name_plural = "Удельный вес протяженности"
