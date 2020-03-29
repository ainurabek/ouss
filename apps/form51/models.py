from django.db import models

# Create your models here.
from apps.customer.models import Customer
from apps.objects.models import Trassa, Object

from apps.accounts.models import Profile




class Region(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=30, unique=True)


	class Meta:
		verbose_name = 'Область'
		verbose_name_plural = 'Список областей'

	def __str__(self):
		return (self.name or '')

class Form51(models.Model):
	trassa = models.ForeignKey(Trassa, on_delete=models.CASCADE, blank=True, null=True, related_name='trassa_form51')
	num=models.CharField('Номер задейственного канала', max_length=100, blank=True, null=True)
	direction = models.CharField('Направление основного пути', max_length=100, blank=True, null=True)
	customer=models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_form51' )
	object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
	amount_inst_channels = models.CharField('Количество монтированных каналов', max_length=100, blank=True, null=True)
	amount_inv_channels = models.CharField('Количество задействованных каналов', max_length=100, blank=True, null=True)
	year = models.CharField('Год ввода', max_length=100, blank=True, null=True)
	order = models.ImageField('Распоряжение', upload_to='object/order/', blank=True)
	schema= models.ImageField('Схема', upload_to='object/schema/', blank=True)
	reserve = models.BooleanField('Наличие резерва', blank=True, null=True)
	region=models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, related_name='region_form51' )


	class Meta:
		verbose_name = 'Форма 5.1'
		verbose_name_plural = 'Форма 5.1.'

	def __str__(self):
		return self.trassa
