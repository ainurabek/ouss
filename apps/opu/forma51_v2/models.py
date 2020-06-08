from django.db import models
from apps.opu.objects.models import Object
from apps.opu.customer.models import Customer

class Category_Form(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name

class Forma(models.Model):
	object = models.ForeignKey(Object, blank=True, null=True, on_delete=models.CASCADE)
	direction = models.CharField('Напр.основ.пути', max_length=255, blank=True, null=True)
	amount_inst_channels = models.CharField('Количество монтированных каналов', max_length=100, blank=True, null=True)
	amount_inv_channels = models.CharField('Количество задействованных каналов', max_length=100, blank=True, null=True)
	year = models.CharField('Год ввода', max_length=100, blank=True, null=True)
	reserve = models.BooleanField('Наличие резерва', blank=True, null=True)
	order = models.CharField('Распоряжение', max_length=255, blank=True, null=True)
	customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)
	category = models.ForeignKey(Category_Form, blank=True, null=True, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Форма 5.1'
		verbose_name_plural = 'Форма 5.1.'

	def __str__(self):
		return str(self.id)
