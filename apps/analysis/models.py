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
    length_kls = models.FloatField("Протяженность кан*км КЛС", default=0, blank=True, null=True)
    downtime_kls = models.FloatField("Простои КЛС", default=0, blank=True, null=True)
    coefficient_kls = models.IntegerField("Коэффициент качества КЛС", default=0, blank=True, null=True)

    outfit_period_of_time_vls = models.FloatField("Продолжительность всех ПВ кан*час ВЛС", blank=True, null=True, default=0)
    length_vls = models.FloatField("Протяженность кан*км ВЛС", default=0, blank=True, null=True)
    downtime_vls = models.FloatField("Простои ВЛС", default=0, blank=True, null=True)
    coefficient_vls = models.IntegerField("Коэффициент качества ВЛС", default=0, blank=True, null=True)

    outfit_period_of_time_rrl = models.FloatField("Продолжительность всех ПВ кан*час РРЛ", blank=True, null=True, default=0)
    length_rrl = models.FloatField("Протяженность кан*км РРЛ", default=0, blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if self.outfit is not None:
            self.outfit.length_kls = self.length_kls
            self.outfit.length_vls = self.length_vls
            self.outfit.length_rrl = self.length_rrl
            self.outfit.save()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if self.outfit is not None:
            self.outfit.total_number_kls = self.total_number_kls
            self.outfit.corresponding_norm_kls = self.corresponding_norm_kls
            self.outfit.total_number_vls = self.total_number_vls
            self.outfit.corresponding_norm_vls = self.corresponding_norm_vls
            self.outfit.total_number_rrl = self.total_number_rrl
            self.outfit.corresponding_norm_rrl = self.corresponding_norm_rrl
            self.outfit.save()
        super().save(*args, **kwargs)



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


class MethodLaying(models.Model):
    name = models.CharField("Название", max_length=150)
    is_read_only = models.BooleanField(default=False)  # if True - то название нельзя редактировать

    class Meta:
        verbose_name = "Способ прокладки"
        verbose_name_plural = "Способы прокладки"

    def __str__(self):
        return self.name

class TypeCable(models.Model):
    name = models.CharField("Название", max_length=150)
    class Meta:
        verbose_name = "Тип кабеля"
        verbose_name_plural = "Тип кабеля"

    def __str__(self):
        return self.name

class TypeConnection(models.Model):
    name = models.CharField("Название", max_length=150)
    class Meta:
        verbose_name = "Тип связи"
        verbose_name_plural = "Тип связи"

    def __str__(self):
        return self.name

class TypeEquipment(models.Model):
    name = models.CharField("Название", max_length=150)
    class Meta:
        verbose_name = "Тип аппаратуры"
        verbose_name_plural = "Тип аппаратуры"

    def __str__(self):
        return self.name

class Form61KLS(models.Model):
    point1 = models.ForeignKey(Point, related_name='form61_KLS_point', verbose_name='ИП от', on_delete=models.SET_NULL,
                               blank=True, null=True)
    point2 = models.ForeignKey(Point, related_name='form61_KLS_point2', verbose_name='ИП до', on_delete=models.SET_NULL,
                               blank=True, null=True)
    total_length_line = models.FloatField("Общая протяженность линии КЛС", default=0, blank=True, null=True)
    total_length_cable = models.FloatField("Общая протяженность кабеля КЛС", default=0, blank=True, null=True)

    above_ground= models.FloatField("Проложено над землей", default=0, blank=True, null=True)
    under_ground = models.FloatField("Проложено под землей", default=0, blank=True, null=True)

    year_of_laying = models.CharField("Год прокладки", max_length=255, blank=True, null=True)
    laying_method = models.ManyToManyField(MethodLaying,  verbose_name="Способ прокладки", related_name='form61_methods')
    type_cable = models.ForeignKey(TypeCable, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name="Тип кабеля")
    type_connection = models.ForeignKey(TypeConnection, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name="Тип Связи", related_name='form61_KLS_connection')
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия", related_name='form61_KLS_out')
    src = models.ImageField('Схема', upload_to='files/', blank=True)



    def __str__(self):
        return f"{self.point1.name}-{self.point2.name}"

    class Meta:
        verbose_name = "Форма 61 (ВОЛС)"
        verbose_name_plural = "Форма 61 (ВОЛС)"

class Form61RRL(models.Model):
    point1 = models.ForeignKey(Point, related_name='form61_RRL_point', verbose_name='ИП от', on_delete=models.SET_NULL,
                               blank=True, null=True)
    point2 = models.ForeignKey(Point, related_name='form61_RRL_point2', verbose_name='ИП до', on_delete=models.SET_NULL,
                               blank=True, null=True)
    total_length_line = models.FloatField("Общая протяженность линии РРЛ", default=0, blank=True, null=True)
    type_equipment = models.ForeignKey(TypeEquipment, related_name = 'type_equipment_rrl', verbose_name= 'Тип аппаратуры',
                                       on_delete=models.SET_NULL, blank=True, null=True)
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, related_name='form61_RRL_out',
                               verbose_name="Предприятия")
    type_connection = models.ForeignKey(TypeConnection, on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name="Тип Связи", related_name='form61_RRL_connection')
    src = models.ImageField('Схема', upload_to='files/', blank=True)



    def __str__(self):
        return f"{self.point1.name}-{self.point2.name}"

    class Meta:
        verbose_name = "Форма 61 (РРЛ)"
        verbose_name_plural = "Форма 61 (РРЛ)"

