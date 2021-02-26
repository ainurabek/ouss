from django.db import models
from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object
from simple_history.models import HistoricalRecords



class Form51(models.Model):
    """Форма 5.1"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Арендатор", blank=True, null=True)
    object = models.OneToOneField(Object, on_delete=models.CASCADE, verbose_name="КО", blank=True, null=True)
    num_order = models.CharField("Номер распоряжения", max_length=250, blank=True, null=True)
    reserve = models.CharField('Наличие резерва', max_length=15, blank=True, null=True)
    # reserve_object = models.ManyToManyField(Object, verbose_name="Трасса резерва потока", related_name="reserve_objects", blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    comments = models.CharField('Примечание', max_length=400, blank=True, null=True)
    history = HistoricalRecords(related_name='history_form51_log')

    class Meta:
        verbose_name = 'Форма 5.1'
        verbose_name_plural = 'Форма 5.1.'
        ordering = ('id',)

    def __str__(self):
        return self.object.name



class SchemaPhoto(models.Model):
    src = models.FileField('Схема', upload_to='files/', blank=True, null=True)
    form51 = models.ForeignKey(Form51, on_delete=models.CASCADE, verbose_name="Схема",
                                 blank=True, null=True, related_name="schema_photo")


class OrderPhoto(models.Model):
    src = models.FileField('Схема', upload_to='files/', blank=True, null=True)
    form51 = models.ForeignKey(Form51, on_delete=models.CASCADE, verbose_name="Распоряжение",
                                 blank=True, null=True, related_name="order_photo")