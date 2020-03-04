from django.db import models

# Create your models here.
from apps.customer.models import Customer

from apps.accounts.models import Profile
from django.db.models.signals import post_save


class TraktOrLine(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Линия/Тракт'
		verbose_name_plural = 'Линия/Тракт'


class InOut(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name


class TPO(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True) #название ТПО
	tpo = models.CharField('Индекс', max_length=100, blank=True, null=True) #номер ТПО

	class Meta:
		verbose_name = 'ТПО'
		verbose_name_plural = 'ТПО'

	def __str__(self):
		return f'{self.name}, {self.tpo}'


class TypeOfTrakt(models.Model):
	index = models.CharField('Индекс', max_length=100, blank=True, null=True)
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	group = models.CharField('Группа', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Тип тракта'
		verbose_name_plural = 'Тип тракта'

	def __str__(self):
		return self.name


class TypeOfLocation(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Тип принадлежности'
		verbose_name_plural = 'Тип принадлежности'

	def __str__(self):
		return self.name

class LineType(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)


	class Meta:
		verbose_name = 'Тип линии'
		verbose_name_plural = 'Типы линии'

	def __str__(self):
		return f'{self.name}, {self.id}'

class Category(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	# _id = models.CharField('Индекс', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return f'{self.name}, {self.id}'

class System(models.Model):
	name = models.CharField('Название', max_length=100, blank=True, null=True)

	class Meta:
		verbose_name = 'Вид системы'
		verbose_name_plural = 'Вид системы'

	def __str__(self):
		return f'{self.name}, {self.id}'


class Outfit(models.Model):

	outfit = models.CharField('Аббревиатура', max_length=100, blank=True, null=True)
	adding = models.CharField('Название', max_length=100, blank=True, null=True)
	num_outfit = models.CharField('Номер', max_length=100, blank=True, null=True)
	tpo = models.ForeignKey('TPO', on_delete=models.CASCADE, db_constraint=False, blank=True, null=True)
	type_outfit = models.ForeignKey(TypeOfLocation, related_name='out_tpo', on_delete=models.CASCADE, blank=True,
									null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


	class Meta:
		verbose_name = 'Предприятие'
		verbose_name_plural = 'Предприятия'

	def __str__(self):
		return self.outfit


class Point(models.Model):
	point = models.CharField('ИП', max_length=100, blank=True, null=True)
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	id_outfit = models.ForeignKey(Outfit, related_name='point_out', on_delete=models.CASCADE, blank=True, null=True)
	tpo = models.ForeignKey('TPO', db_constraint=False, related_name='point_tpo', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.point

class Trassa(models.Model):
	name = models.CharField(max_length=1000, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name = 'Трасса'
		verbose_name_plural = 'Трасса'

	def __str__(self):
		return self.name

class Object(models.Model):
	'''Линии Передачи, Тракт , ВГ-ПГ'''
	trassa = models.ForeignKey(Trassa, related_name='object_trasa', on_delete=models.CASCADE, blank=True, null=True)
	# id_object = models.CharField(max_length=100, blank=True, null=True)
	id_parent = models.ForeignKey('Object', on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField('Название', max_length=100, blank=True, null=True)
	COreceive = models.CharField('КО прием', max_length=100, blank=True, null=True)
	COdeliver = models.CharField('КО передачи', max_length=100, blank=True, null=True)
	inter_code = models.CharField('Международное обозначение', max_length=100, blank=True, null=True)
	id_outfit = models.ForeignKey(Outfit, related_name='obj_out',on_delete=models.CASCADE, blank=True, null=True)
	tpo1 = models.ForeignKey(TPO, related_name='obj_tpo', on_delete=models.CASCADE, blank=True, null=True)
	point1 = models.ForeignKey(Point, related_name='obj_point', verbose_name='ИП приема', on_delete=models.CASCADE, blank=True, null=True)
	tpo2 = models.ForeignKey(TPO, related_name='obj_tpo2', on_delete=models.CASCADE, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='obj_point2', verbose_name='ИП пер', on_delete=models.CASCADE, blank=True, null=True)
	category = models.ForeignKey(Category, related_name='obj_category', on_delete=models.CASCADE, blank=True, null=True)
	trakt = models.BooleanField(blank=True, null=True)
	num = models.CharField('Номер задейственного канала', max_length=100, blank=True, null=True)
	system = models.ForeignKey(System, related_name='obj_system', on_delete=models.CASCADE, blank=True, null=True)
	main = models.BooleanField()
	_complex = models.BooleanField()
	type_transit1 = models.CharField('Тип транзита1', max_length=100, blank=True, null=True)
	type_transit2 = models.CharField('Тип транзита2', max_length=100, blank=True, null=True)
	id_transit1 = models.ForeignKey('Object', related_name='transit_obj', on_delete=models.CASCADE, blank=True, null=True)
	id_transit2 = models.ForeignKey('Object', related_name='transit2_obj', on_delete=models.CASCADE, blank=True, null=True)
	comments = models.CharField('Примечание', max_length=100, blank=True, null=True)
	handel_add_path1 = models.CharField('Начало', max_length=100, blank=True, null=True)
	handel_add_path2 = models.CharField('Конец', max_length=100, blank=True, null=True)
	destination1 = models.ForeignKey('IP', related_name='obj_dest1', on_delete=models.CASCADE, blank=True, null=True)
	destination2 = models.ForeignKey('IP', related_name='obj_dest2', on_delete=models.CASCADE, blank=True, null=True)
	our = models.ForeignKey(TypeOfLocation, related_name='obj_our', on_delete=models.CASCADE, blank=True, null=True)
	amount_channels = models.CharField('Количество каналов', max_length=100, blank=True, null=True)
	not_in_use = models.BooleanField('Активный/Нет')
	type_line = models.ForeignKey(LineType, related_name='obj_type_line',on_delete=models.CASCADE, blank=True, null=True)
	type_of_trakt = models.ForeignKey(TypeOfTrakt, related_name='obj_trakt_type', on_delete=models.CASCADE, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='obj_cust', on_delete=models.CASCADE, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name = 'Линия передачи/Обьект/Тракт'
		verbose_name_plural = 'Линия передачи/Обьект/Тракт'

	def __str__(self):
		return self.name

class IP(models.Model):
	point_id = models.ForeignKey(Point, on_delete=models.CASCADE, blank=True, null=True)
	object_id = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
	tpo_id = models.ForeignKey(TPO, on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		verbose_name = 'ИП'
		verbose_name_plural = 'ИП'

	def __str__(self):
		return self.point_id.point


class TransitObject(models.Model):
	id_complex_object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_complex_obj')
	id_object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='id_transit_obj')
	num = models.CharField(max_length=100, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)



