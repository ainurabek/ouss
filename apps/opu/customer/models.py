from django.db import models

# Create your models here.

class Customer(models.Model):
	customer = models.CharField('Название', max_length=250, blank=True, null=True)
	abr = models.CharField('Абревиатура', max_length=100, blank=True, null=True)
	address = models.CharField('Адрес', max_length=250, blank=True, null=True)
	email = models.EmailField('Email', max_length=250, blank=True, null=True)
	adding = models.CharField('Ответственное лицо', max_length=200, blank=True, null=True)
	reuisits = models.CharField('Реквизиты', max_length=200, blank=True, null=True)
	our_services_to = models.CharField('Наши услуги', max_length=200, blank=True, null=True)
	connection_points = models.CharField('Точки подключения', max_length=200, blank=True, null=True)
	created_at = models.DateField('Дата', auto_now_add=True)


	class Meta:
		verbose_name = 'Арендатор'
		verbose_name_plural = 'Арендаторы'

	def __str__(self):
		return self.abr






