from django.db import models
from simple_history.models import HistoricalRecords


class Customer(models.Model):
	customer = models.CharField('Название', max_length=250)
	abr = models.CharField('Абревиатура', max_length=100)
	address = models.CharField('Адрес', max_length=250, blank=True, null=True)
	email = models.CharField('Email и телефон', max_length=1250, blank=True, null=True)
	diapozon = models.CharField('Диапозон нумераций', max_length=1250, blank=True, null=True)
	created_at = models.DateField('Дата', auto_now_add=True)
	adding = models.CharField("Примечание", max_length=250, blank=True, null=True)
	history = HistoricalRecords(related_name='history_customer_log')

	class Meta:
		verbose_name = 'Арендатор'
		verbose_name_plural = 'Арендаторы'
		ordering = ('id',)

	def __str__(self):
		return self.abr






