from django.db import models

from apps.accounts.models import Profile
from apps.opu.objects.models import Outfit, MainLineType


class OutfitItem5(models.Model):
    id_parent = models.ForeignKey("OutfitItem5", on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="Республика", related_name="parent_out")
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия")
    total_coefficient = models.OneToOneField("SpecificGravityOfLength", on_delete=models.CASCADE,
                                             verbose_name="Удельный вес протяженности")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Предприятия"
        verbose_name_plural = "Предприятия"


class Item5(models.Model):
    """ П.5 """
    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)
    outfit_period_of_time = models.FloatField("Продолжительность всех ПВ кан*час", blank=True, null=True, default=0)
    length = models.FloatField("Протяженность кан*км", default=0, blank=True, null=True)
    downtime = models.FloatField("Простои", default=0, blank=True, null=True)
    coefficient = models.IntegerField("Коэффициент качества", default=0, blank=True, null=True)
    type_line = models.ForeignKey(MainLineType, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name="Тип линии")
    outfit_item5 = models.ForeignKey(OutfitItem5, on_delete=models.CASCADE, related_name="item5", blank=True,
                                     null=True, verbose_name="Предприятия")

    class Meta:
        verbose_name = "п.5"
        verbose_name_plural = "п.5"

    def __str__(self):
        return f"{self.id}"


class SpecificGravityOfLength(models.Model):
    """Удельный вес протяженности"""
    id_parent = models.ForeignKey("SpecificGravityOfLength", on_delete=models.CASCADE, blank=True, null=True)
    total_length = models.FloatField("Общая протяж. кан*км", default=0, blank=True, null=True)
    coefficient = models.FloatField("Коэффициент качества", default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Удельный вес протяженности"
        verbose_name_plural = "Удельный вес протяженности"


class SpecificGravityOfLengthTypeLine(models.Model):
    """Тип линии"""
    type_line = models.ForeignKey(MainLineType, on_delete=models.SET_NULL, blank=True,
                                  null=True, verbose_name="Тип линии")
    value = models.FloatField("Значение", default=0, blank=True, null=True)
    specific_gravity_of_length = models.ForeignKey(SpecificGravityOfLength, on_delete=models.CASCADE,
                                                   blank=True, null=True, related_name="space",
                                                   verbose_name="Удельный вес протяженности")
    type_line_value = models.OneToOneField(Item5, related_name="type_line_value",
                                           blank=True, null=True, on_delete=models.CASCADE)
    type_line_value7 = models.OneToOneField("Item7", related_name="type_line_value7",
                                           blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.value}"

    class Meta:
        verbose_name = "Тип линии"
        verbose_name_plural = "Типы линии"


class Item7(models.Model):
    total_object = models.IntegerField("Общее количество линейных трактов", default=0, blank=True, null=True)
    corresponding_norm = models.IntegerField("Соответствующих норме", default=0, blank=True, null=True)
    match_percentage = models.IntegerField("Процент соответствия", default=0, blank=True, null=True)
    coefficient = models.IntegerField("Коэффициент качества", default=0, blank=True, null=True)
    type_line = models.ForeignKey(MainLineType, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name="Тип линии")
    outfit_item5 = models.ForeignKey(OutfitItem5, on_delete=models.CASCADE, related_name="item7", blank=True,
                                     null=True, verbose_name="Предприятия")
    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "п.7"
        verbose_name_plural = "п.7"

    def __str__(self):
        return f"{self.id}"


class FormAnalysis(models.Model):
    id_parent = models.ForeignKey("FormAnalysis", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Название", max_length=255)
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Предприятия")
    coefficient_item5 = models.OneToOneField(OutfitItem5, on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name="п.5", related_name="form_item5")
    coefficient_item7 = models.OneToOneField(OutfitItem5, on_delete=models.CASCADE, blank=True, null=True,
                                          verbose_name="п.7", related_name="form_item7")
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_coefficient = models.FloatField("Средний коэффициент качества", default=0, blank=True, null=True)
    coefficient = models.FloatField("Коэффициент качества", default=0, blank=True, null=True)
    date_from = models.DateField("Начало", blank=True, null=True)
    date_to = models.DateField("Конец", blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "ср.Кфт"
        verbose_name_plural = "ср.Кфт"
