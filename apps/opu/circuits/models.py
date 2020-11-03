from django.db import models
# Create your models here.
from apps.opu.objects.models import IP, Object, Category, InOut, Point
from apps.opu.customer.models import Customer
from sortedm2m.fields import SortedManyToManyField
from simple_history.models import HistoricalRecords

from apps.accounts.models import Profile


class Measure(models.Model):

	name = models.CharField('Название', max_length=100)

	def __str__(self):
		return f'{self.name}, {self.id}'

class Speed(models.Model):

	name = models.CharField('Название', max_length=100)

	class Meta:
		verbose_name = 'Скорость'
		verbose_name_plural = 'Скорость'

	def __str__(self):
		return f'{self.name}, {self.id}'

class TypeCom(models.Model):
	name = models.CharField('Название', max_length=100)


	class Meta:
		verbose_name = 'Тип коммуникации'
		verbose_name_plural = 'Типы коммуникации'

	def __str__(self):
		return f'{self.name}, {self.id}'

class Mode(models.Model):
	name = models.CharField('Название', max_length=100)

	class Meta:
		verbose_name = 'Режим'
		verbose_name_plural = 'Режимы'

	def __str__(self):
		return f'{self.name}, {self.id}'




class Circuit(models.Model):
	"""Каналы"""

	id_parent = models.ForeignKey('Circuit', on_delete=models.CASCADE, blank=True, null=True)
	num_circuit = models.CharField('Номер канала', max_length=100, blank=True, null=True)
	final_destination = models.ForeignKey(Point, related_name='circ_final_dest',on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(unique=True, max_length=100, blank=True, null=True)
	type_using = models.CharField(max_length=100, blank=True, null=True)
	category = models.ForeignKey(Category, related_name='circ_cat',on_delete=models.SET_NULL, blank=True, null=True) ###
	num_order = models.CharField(max_length=100, blank=True, null=True)
	date_order = models.CharField(max_length=100, blank=True, null=True)
	num_arenda = models.CharField(max_length=100, blank=True, null=True)
	number = models.CharField('Номер', max_length=100, blank=True, null=True)
	speed = models.CharField(max_length=100, blank=True, null=True)
	measure = models.ForeignKey(Measure, related_name='circ_measure', on_delete=models.SET_NULL, blank=True, null=True)
	adding = models.CharField('Примечание', max_length=100, blank=True, null=True)
	comments = models.CharField(max_length=100, blank=True, null=True)

	transit = SortedManyToManyField("Circuit", related_name='cir_transit_obj1', blank=True)
	transit2 = SortedManyToManyField("Circuit", related_name='cir_transit_obj2', blank=True)
	in_out = models.ForeignKey(InOut, related_name='circ_in', on_delete=models.SET_NULL, blank=True, null=True)
	first = models.BooleanField('Используется/Не используется', default = False)

	point1 = models.ForeignKey(Point, related_name='circ_ip1', on_delete=models.SET_NULL, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='circ_ip2', on_delete=models.SET_NULL, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='circ_cust', on_delete=models.SET_NULL, blank=True, null=True)
	id_object = models.ForeignKey(Object, related_name='circ_obj', on_delete=models.CASCADE, blank=True, null=True)
	mode = models.ForeignKey(Mode, related_name='circ_mode', on_delete=models.SET_NULL, blank=True, null=True)
	type_com = models.ForeignKey(TypeCom, related_name='circ_type_com', on_delete=models.SET_NULL, blank=True, null=True)

	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	history = HistoricalRecords(related_name='history_circuit_log')

	class Meta:
		verbose_name = 'Канал для Формы 5.3'
		verbose_name_plural = 'Каналы для Формы 5.3'
		ordering = ('id',)

	def __str__(self):
		return self.name

class Bypass(models.Model):

	num = models.CharField(max_length=100, blank=True, null=True)
	num_p = models.CharField(max_length=100, blank=True, null=True)
	id_main = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True, related_name='bypass_id_main')
	id_bypass = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True, related_name='id_bypass')


class AssignPart(models.Model):

	id_object_main =  models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_obj_main')
	id_object_part =  models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_obj_part')


