from django.db import models

# Create your models here.


class Signalization(models.Model):
	name=models.CharField('Название', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Сигнализация'
		verbose_name_plural = 'Сигнализация'

	def __str__(self):
		return self.name


class Customer(models.Model):
	customer = models.CharField('Название', max_length=250, blank=True, null=True)
	abr = models.CharField('Абревиатура', max_length=100, blank=True, null=True)
	address = models.CharField('Адрес', max_length=250, blank=True, null=True)
	email = models.EmailField('Email', max_length=250, blank=True, null=True)
	contact_name = models.CharField('Ответственное лицо', max_length=200, blank=True, null=True)
	reuisits = models.CharField('Реквизиты', max_length=200, blank=True, null=True)
	created_at = models.DateField('Дата', auto_now_add=True)
	amount_flow=models.CharField('Количество потоков', max_length=200, blank=True, null=True)
	signalization=models.ForeignKey(Signalization,  related_name='cust_sign', on_delete=models.CASCADE, blank=True, null=True)
	type_of_using=models.CharField('Вид использования', max_length=200, blank=True, null=True)
	num_order = models.CharField("Номер распоряжения", max_length=250, blank=True, null=True)
	order = models.ImageField('Распоряжение', upload_to='object/order/', blank=True, null=True)
	comments = models.CharField("Примечание", max_length=250, blank=True, null=True)


	class Meta:
		verbose_name = 'Арендатор'
		verbose_name_plural = 'Арендаторы'

	def __str__(self):
		return self.abr






