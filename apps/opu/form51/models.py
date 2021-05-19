from django.db import models
from apps.accounts.models import Profile
from apps.opu.customer.models import Customer
from apps.opu.objects.models import Object
from simple_history.models import HistoricalRecords


class Form51(models.Model):
    """Форма 5.1"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Арендатор", blank=True, null=True)
    object = models.OneToOneField(Object, on_delete=models.CASCADE, verbose_name="КО")
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    comments = models.TextField('Примечание', blank=True, null=True)
    history = HistoricalRecords(related_name='history_form51_log')

    class Meta:
        verbose_name = 'Форма 5.1'
        verbose_name_plural = 'Форма 5.1.'
        ordering = ('object',)

    def __str__(self):
        return self.object.name
