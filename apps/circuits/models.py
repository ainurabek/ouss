from django.db import models
# Create your models here.
from apps.objects.models import IP, Object, Category, InOut
from apps.customer.models import Customer

from apps.accounts.models import Profile


class Measure(models.Model):
	index = models.CharField('Индекс', max_length=100, blank=True, null=True)
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.name}, {self.index}'

class Speed(models.Model):
	index = models.CharField('Индекс', max_length=100, blank=True, null=True)
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Скорость'
		verbose_name_plural = 'Скорость'

	def __str__(self):
		return self.name

class Type(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	_id = models.CharField('Индекс', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Тип коммуникации'
		verbose_name_plural = 'Типы коммуникации'

	def __str__(self):
		return f'{self.name}, {self._id}'

class Mode(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	_id = models.CharField('Индекс', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Режим'
		verbose_name_plural = 'Режимы'

	def __str__(self):
		return self.name


class SubsRoutes(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	route = models.CharField(max_length=100, blank=True, null=True)

class Circuit(models.Model):
	"""Каналы"""
	id_circuit = models.CharField(max_length=100, blank=True, null=True)
	id_parent = models.ForeignKey('Circuit', on_delete=models.CASCADE, blank=True, null=True)
	num_circuit = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	type_using = models.CharField(max_length=100, blank=True, null=True)#######
	category = models.ForeignKey(Category, related_name='circ_category', on_delete=models.CASCADE, blank=True, null=True) ###
	num_order = models.CharField(max_length=100, blank=True, null=True)
	date_order = models.CharField(max_length=100, blank=True, null=True)
	num_arenda = models.CharField(max_length=100, blank=True, null=True)
	number = models.CharField('Номер телефона', max_length=100, blank=True, null=True)
	speed = models.ForeignKey(Speed, related_name='circ_speed', on_delete=models.CASCADE, blank=True, null=True)
	measure = models.ForeignKey(Measure, related_name='circ_measure', on_delete=models.CASCADE, blank=True, null=True)
	adding = models.CharField(max_length=100, blank=True, null=True)
	comments = models.CharField(max_length=100, blank=True, null=True)
	type_transit1 = models.CharField(max_length=100, blank=True, null=True)
	type_transit2 = models.CharField(max_length=100, blank=True, null=True)
	id_transit1 = models.CharField(max_length=100, blank=True, null=True)
	id_transit2 = models.CharField(max_length=100, blank=True, null=True)
	in_out = models.ForeignKey(InOut, related_name='circ_in', on_delete=models.CASCADE, blank=True, null=True)
	first = models.BooleanField()
	handel_add_path1 = models.CharField(max_length=100, blank=True, null=True)
	handel_add_path2 = models.CharField(max_length=100, blank=True, null=True)
	destination1 = models.ForeignKey(IP, related_name='circ_ip1', on_delete=models.CASCADE, blank=True, null=True)
	destination2 = models.ForeignKey(IP, related_name='circ_ip2', on_delete=models.CASCADE, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='circ_cust', on_delete=models.CASCADE, blank=True, null=True)
	id_object = models.ForeignKey(Object, related_name='circ_obj', on_delete=models.CASCADE, blank=True, null=True)
	mode = models.ForeignKey(Mode, related_name='circ_mode', on_delete=models.CASCADE, blank=True, null=True)
	type_com = models.ForeignKey(Type, related_name='circ_type_com', on_delete=models.CASCADE, blank=True, null=True)
	id_subst =  models.ForeignKey(SubsRoutes, related_name='circ_subst', on_delete=models.CASCADE, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Канал'
		verbose_name_plural = 'Каналы'

class Bypass(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	num = models.CharField(max_length=100, blank=True, null=True)
	num_p = models.CharField(max_length=100, blank=True, null=True)
	id_main = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True, related_name='bypass_id_main')
	id_bypass = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True, related_name='id_bypass')


class AssignPart(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	id_object_main =  models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_obj_main')
	id_object_part =  models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_obj_part')


