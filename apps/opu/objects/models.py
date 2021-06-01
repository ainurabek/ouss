# coding: utf-8

from django.db import models
# Create your models here.
from apps.opu.customer.models import Customer
from apps.accounts.models import Profile

from sortedm2m.fields import SortedManyToManyField
from simple_history.models import HistoricalRecords



class Bug(models.Model):
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)

	class Meta:
		verbose_name = 'Ошибка'
		verbose_name_plural = 'Ошибки'


class TPO(models.Model):
	name = models.CharField('Название', max_length=500, error_messages={"invalid": "Это поле обязательно."}) #название ТПО
	index = models.CharField('Индекс', max_length=500) #номер ТПО

	class Meta:
		verbose_name = 'ТПО'
		verbose_name_plural = 'ТПО'

	def __str__(self):
		return f'{self.name},{self.index}, {self.id}'


class TypeOfTrakt(models.Model):
	name = models.CharField('Название', max_length=500)

	class Meta:

		verbose_name = 'ПГ/ВГ/ТГ/ЧГ/РГ'
		verbose_name_plural = 'ПГ/ВГ/ТГ/ЧГ/РГ'

	def __str__(self):
		return self.name


class TypeOfLocation(models.Model):

	name = models.CharField('Название', max_length=500)

	class Meta:
		verbose_name = 'Тип принадлежности'
		verbose_name_plural = 'Тип принадлежности'

	def __str__(self):
		return self.name


class MainLineType(models.Model):
	name = models.CharField(max_length=550)

	class Meta:
		verbose_name = 'Тип линии АК'
		verbose_name_plural = 'Типы линии АК'

	def __str__(self):
		return self.name


class LineType(models.Model):
	name = models.CharField('Название', max_length=500)
	main_line_type = models.ForeignKey(MainLineType, related_name="main_line_type", on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		verbose_name = 'Тип линии'
		verbose_name_plural = 'Типы линии'

	def __str__(self):
		return f'{self.name}, {self.id}'


class Category(models.Model):
	index = models.CharField('Индекс', max_length=500)
	name = models.CharField('Обозначение', max_length=500)

	class Meta:
		verbose_name = 'Индекс назначения КО'
		verbose_name_plural = 'Индекс назначения КО'

	def __str__(self):
		return f'{self.index}, {self.id}'


class Outfit(models.Model):
	outfit = models.CharField('Аббревиатура', max_length=500, blank=True, null=True)
	adding = models.CharField('Название', max_length=500)
	num_outfit = models.CharField('Номер', max_length=500, blank=True, null=True)
	tpo = models.ForeignKey('TPO', null = True, on_delete=models.SET_NULL)
	type_outfit = models.ForeignKey('TypeOfLocation', null = True, on_delete=models.SET_NULL)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	history = HistoricalRecords(related_name='history_outfit_log')

	length_kls = models.FloatField("Протяженность кан*км КЛС", default=0, blank=True, null=True)
	length_vls = models.FloatField("Протяженность кан*км ВЛС", default=0, blank=True, null=True)
	length_rrl = models.FloatField("Протяженность кан*км РРЛ", default=0, blank=True, null=True)

	total_number_kls = models.IntegerField("Общее количество линейных трактов КЛС", default=0, blank=True, null=True)
	corresponding_norm_kls = models.IntegerField("Соответствующих норме КЛС", default=0, blank=True, null=True)
	total_number_vls = models.IntegerField("Общее количество линейных трактов ВЛС", default=0, blank=True, null=True)
	corresponding_norm_vls = models.IntegerField("Соответствующих норме ВЛС", default=0, blank=True, null=True)
	total_number_rrl = models.IntegerField("Общее количество линейных трактов РРЛ", default=0, blank=True, null=True)
	corresponding_norm_rrl = models.IntegerField("Соответствующих норме РРЛ", default=0, blank=True, null=True)

	class Meta:
		verbose_name = 'Предприятие'
		verbose_name_plural = 'Предприятия'

	def __str__(self):
		return self.outfit


class OutfitWorker(models.Model):
	name = models.CharField('ФИО', max_length=500)
	outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='outfit_worker')

	class Meta:
		verbose_name = 'Сотрудник предприятия'
		verbose_name_plural = 'Сотрудники предприятий'
		ordering = ('id',)

	def __str__(self):
		return self.name


class Point(models.Model):
	point = models.CharField('ИП', max_length=500, unique=True)
	name = models.CharField('Название', max_length=100)
	id_outfit = models.ForeignKey(Outfit, related_name='point_out', on_delete=models.CASCADE, blank=True, null=True)
	tpo = models.ForeignKey(TPO, related_name='point_tpo', on_delete=models.CASCADE, blank=True, null=True)
	region = models.CharField('Район', max_length=550, blank=True, null=True)
	type_equipment = models.CharField('Тип оборудования', max_length=550, blank=True, null=True)
	total_point_channels_KLS = models.IntegerField("Значение_КЛС", default=0)
	total_point_channels_RRL = models.IntegerField("Значение_ЦРРЛ", default=0)
	history = HistoricalRecords(related_name='history_point_log')

	def __str__(self):
		return self.point


class AmountChannel(models.Model):
	name = models.CharField("Название", max_length=550)
	value = models.IntegerField("Значение")
	is_read_only = models.BooleanField(default=False) #if True - то название канала нельзя редактировать

	class Meta:
		verbose_name = "Количество каналов"
		verbose_name_plural = "Количество каналов"

	def __str__(self):
		return self.name


class Consumer(models.Model):
	name = models.CharField("Название", max_length=550)

	class Meta:
		verbose_name = "Потребитель"
		verbose_name_plural = "Потребители"

	def __str__(self):
		return self.name


class Object(models.Model):
	'''Линии Передачи, Тракт , ВГ-ПГ'''
	id_parent = models.ForeignKey('Object', on_delete=models.CASCADE, related_name='parents', blank=True, null=True)
	name = models.CharField('Название', max_length=500)
	id_outfit = models.ForeignKey(Outfit, related_name='obj_out',on_delete=models.SET_NULL, blank=True, null=True)
	tpo1 = models.ForeignKey(TPO, related_name='obj_tpo', on_delete=models.SET_NULL, blank=True, null=True)
	point1 = models.ForeignKey(Point, related_name='obj_point', verbose_name='ИП приема', on_delete=models.SET_NULL, blank=True, null=True)
	tpo2 = models.ForeignKey(TPO, related_name='obj_tpo2', on_delete=models.SET_NULL, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='obj_point2', verbose_name='ИП пер', on_delete=models.SET_NULL, blank=True, null=True)
	category = models.ForeignKey('Category', related_name='obj_category', on_delete=models.SET_NULL, blank=True, null=True)
	comments = models.CharField('Примечание', max_length=500, blank=True, null=True)
	comments_GOZ = models.CharField('Примечание(ГОЗ)', max_length=500, blank=True, null=True)
	our = models.ForeignKey(TypeOfLocation, related_name='obj_our', on_delete=models.SET_NULL, blank=True, null=True)
	amount_channels = models.ForeignKey(AmountChannel, related_name='object_channel', verbose_name='Монтированные каналы',
										blank=True, null=True, on_delete=models.SET_NULL)
	type_line = models.ForeignKey(LineType, related_name='obj_type_line', on_delete=models.SET_NULL, blank=True, null=True)
	type_of_trakt = models.ForeignKey(TypeOfTrakt, related_name='obj_trakt_type', on_delete=models.SET_NULL, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='obj_cust', on_delete=models.CASCADE, blank=True, null=True)
	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	total_amount_channels = models.IntegerField('Задействованные каналы', default=0, blank=True, null=True)
	order = models.CharField('№ и дата распоряжения', max_length=500, blank=True, null=True)
	src = models.ImageField('Скан распоряжения', upload_to='files/', blank=True)
	consumer = models.ForeignKey(Consumer, related_name='obj_consumer', on_delete=models.SET_NULL, blank=True, null=True)
	is_transit = models.BooleanField(default=False)  # if True - то его компоненты участвуют в транзите, при измнении, эти компоненты перезапишутся
	history = HistoricalRecords(related_name='history_object_log')


	class Meta:
		verbose_name = 'Линия передачи/Обьект/Тракт'
		verbose_name_plural = 'Линия передачи/Обьект/Тракт'
		ordering = ('id',)

	def __str__(self):
		return str(self.name)


class IP(models.Model):
	object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='ip_object')
	point_id = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='ip_point')
	tpo_id = models.ForeignKey(TPO, on_delete=models.SET_NULL, null=True, blank=True)
	history = HistoricalRecords(related_name='history_ip_log')

	class Meta:
		verbose_name = 'ИП'
		verbose_name_plural = 'ИПы'
		ordering = ('id',)

	def __str__(self):
		return self.point_id.point


class OrderObjectPhoto(models.Model):
	src = models.FileField(upload_to='files/', blank=True, null=True)
	object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="Распоряжение", blank=True, related_name="order_object_photo")


class Transit(models.Model):
	name = models.CharField(max_length=255)
	trassa = SortedManyToManyField(Object, related_name="transits", blank=True)
	create_circuit_transit = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Bridge(models.Model):
	object = models.ForeignKey(Object, related_name="bridges", on_delete=models.CASCADE)
	transit = models.ForeignKey(Transit, related_name="can_see", on_delete=models.CASCADE)
