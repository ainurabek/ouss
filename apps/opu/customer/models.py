from django.db import models

# Create your models here.

class Customer(models.Model):
	customer = models.CharField('Название', max_length=250)
	abr = models.CharField('Абревиатура', max_length=100)
	address = models.CharField('Адрес', max_length=250, blank=True, null=True)
	email = models.EmailField('Email', max_length=250, blank=True, null=True)
	contact_name = models.CharField('Ответственное лицо', max_length=200, blank=True, null=True)
	reuisits = models.CharField('Реквизиты', max_length=200, blank=True, null=True)
	created_at = models.DateField('Дата', auto_now_add=True)
	adding = models.CharField("Примечание", max_length=250, blank=True, null=True)



	class Meta:
		verbose_name = 'Арендатор'
		verbose_name_plural = 'Арендаторы'
		ordering = ('id',)

	def __str__(self):
		return self.abr






