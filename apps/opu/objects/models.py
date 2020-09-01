from django.db import models

# Create your models here.
from apps.opu.customer.models import Customer

from apps.accounts.models import Profile
from django.db.models.signals import post_save
from sortedm2m.fields import SortedManyToManyField

class InOut(models.Model):
	name = models.CharField('Название', max_length=100)

	def __str__(self):
		return self.name


class TPO(models.Model):
	name = models.CharField('Название', max_length=100, error_messages={"invalid": "Это поле обязательно."}) #название ТПО
	index = models.CharField('Индекс', max_length=100) #номер ТПО

	class Meta:
		verbose_name = 'ТПО'
		verbose_name_plural = 'ТПО'

	def __str__(self):
		return f'{self.name},{self.index}, {self.id}'


class TypeOfTrakt(models.Model):
	name = models.CharField('Название', max_length=100)


	class Meta:
		verbose_name = 'ПГ/ВГ/ТГ/ЧГ/РГ'
		verbose_name_plural = 'ПГ/ВГ/ТГ/ЧГ/РГ'

	def __str__(self):
		return self.name


class TypeOfLocation(models.Model):

	name = models.CharField('Название', max_length=100)

	class Meta:
		verbose_name = 'Тип принадлежности'
		verbose_name_plural = 'Тип принадлежности'

	def __str__(self):
		return self.name


class LineType(models.Model):
	name = models.CharField('Название', max_length=100)


	class Meta:
		verbose_name = 'Тип линии'
		verbose_name_plural = 'Типы линии'

	def __str__(self):
		return f'{self.name}, {self.id}'


class Category(models.Model):
	index = models.CharField('Индекс', max_length=100)
	name = models.CharField('Обозначение', max_length=100)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return f'{self.index}, {self.id}'


class System(models.Model):
	name = models.CharField('Название', max_length=100)

	class Meta:
		verbose_name = 'Вид системы'
		verbose_name_plural = 'Вид системы'

	def __str__(self):
		return f'{self.name}, {self.id}'



class Outfit(models.Model):
	outfit = models.CharField('Аббревиатура', max_length=100, blank=True, null=True)
	adding = models.CharField('Название', max_length=100)
	num_outfit = models.CharField('Номер', max_length=100, blank=True, null=True)
	tpo = models.ForeignKey('TPO', null = True, on_delete=models.SET_NULL)
	type_outfit = models.ForeignKey('TypeOfLocation', null = True, on_delete=models.SET_NULL)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


	class Meta:
		verbose_name = 'Предприятие'
		verbose_name_plural = 'Предприятия'

	def __str__(self):
		return self.outfit

class OutfitWorker(models.Model):
	name = models.CharField('ФИО', max_length=100)
	outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='outfit_worker')

	class Meta:
		verbose_name = 'Сотрудник предприятия'
		verbose_name_plural = 'Сотрудники предприятий'
		ordering = ('id',)

	def __str__(self):
		return self.name

class Point(models.Model):
	point = models.CharField('ИП', max_length=100)
	name = models.CharField('Название', max_length=100)
	id_outfit = models.ForeignKey(Outfit, related_name='point_out', on_delete=models.CASCADE, blank=True, null=True)
	tpo = models.ForeignKey(TPO, related_name='point_tpo', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.point



class Object(models.Model):
	'''Линии Передачи, Тракт , ВГ-ПГ'''
	id_parent = models.ForeignKey('Object', on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField('Название', max_length=100)
	COreceive = models.CharField('КО прием', max_length=100, blank=True, null=True)
	COdeliver = models.CharField('КО передачи', max_length=100, blank=True, null=True)
	inter_code = models.CharField('Международное обозначение', max_length=100, blank=True, null=True)
	id_outfit = models.ForeignKey(Outfit, related_name='obj_out',on_delete=models.SET_NULL, blank=True, null=True)
	tpo1 = models.ForeignKey(TPO, related_name='obj_tpo', on_delete=models.SET_NULL, blank=True, null=True)
	point1 = models.ForeignKey(Point, related_name='obj_point', verbose_name='ИП приема', on_delete=models.SET_NULL, blank=True, null=True)
	tpo2 = models.ForeignKey(TPO, related_name='obj_tpo2', on_delete=models.SET_NULL, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='obj_point2', verbose_name='ИП пер', on_delete=models.SET_NULL, blank=True, null=True)
	category = models.ForeignKey('Category', related_name='obj_category', on_delete=models.SET_NULL, blank=True, null=True)
	trakt= models.BooleanField('Тракт/Линия', blank=True, null=True)
	num = models.CharField('Номер задейственного канала', max_length=100, blank=True, null=True)
	system = models.ForeignKey(System, related_name='obj_system', on_delete=models.SET_NULL, blank=True, null=True)
	type_transit1 = models.CharField('Тип транзита1', max_length=100, blank=True, null=True)
	type_transit2 = models.CharField('Тип транзита2', max_length=100, blank=True, null=True)
	transit = SortedManyToManyField('Object', related_name='transit_obj1', blank=True)
	transit2 = SortedManyToManyField('Object', related_name='transit_obj2', blank=True)
	comments = models.CharField('Примечание', max_length=100, blank=True, null=True)
	handel_add_path1 = models.CharField('Начало', max_length=100, blank=True, null=True)
	handel_add_path2 = models.CharField('Конец', max_length=100, blank=True, null=True)
	destination1 = models.ForeignKey('IP', related_name='obj_dest1', on_delete=models.SET_NULL, blank=True, null=True)
	destination2 = models.ForeignKey('IP', related_name='obj_dest2', on_delete=models.SET_NULL, blank=True, null=True)
	our = models.ForeignKey(TypeOfLocation, related_name='obj_our', on_delete=models.SET_NULL, blank=True, null=True)
	amount_channels = models.CharField('Количество каналов', max_length=100, blank=True, null=True)
	save_in = models.BooleanField('Сохранить', blank=True, null=True)
	type_line = models.ForeignKey(LineType, related_name='obj_type_line',on_delete=models.SET_NULL, blank=True, null=True)
	type_of_trakt = models.ForeignKey(TypeOfTrakt, related_name='obj_trakt_type', on_delete=models.SET_NULL, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='obj_cust', on_delete=models.CASCADE, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	maker_trassa = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='maker', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	add_time = models.DateTimeField(blank=True, null=True)


	class Meta:
		verbose_name = 'Линия передачи/Обьект/Тракт'
		verbose_name_plural = 'Линия передачи/Обьект/Тракт'

	def __str__(self):
		return str(self.name)


class IP(models.Model):
	point_id = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='ip_point')
	object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='ip_object')
	tpo_id = models.ForeignKey(TPO, on_delete=models.SET_NULL, null=True, blank=True)

	class Meta:
		verbose_name = 'ИП'
		verbose_name_plural = 'ИП'

	def __str__(self):
		return self.point_id.point


class TransitObject(models.Model):
	id_complex_object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_complex_obj')
	id_object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_transit_obj')
	num = models.CharField(max_length=100, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

