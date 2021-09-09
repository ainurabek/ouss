from django.db import models
# Create your models here.
from apps.opu.objects.models import IP, Object, Category, Point, Transit
from apps.opu.customer.models import Customer
from sortedm2m.fields import SortedManyToManyField
from simple_history.models import HistoricalRecords
from apps.accounts.models import Profile


class Circuit(models.Model):
	"""Каналы"""

	object = models.ForeignKey(Object, related_name='circuit_object_parent', on_delete=models.CASCADE, blank=True, null=True)
	num_circuit = models.CharField('Номер канала', max_length=100, blank=True, null=True)
	name = models.CharField(unique=True, max_length=100, blank=True, null=True)

	category = models.ForeignKey(Category, related_name='circ_cat', on_delete=models.SET_NULL, blank=True, null=True) ###
	num_order = models.CharField(max_length=100, blank=True, null=True)

	comments = models.CharField(max_length=100, blank=True, null=True)
	first = models.BooleanField('Используется/Не используется', default = True)

	point1 = models.ForeignKey(Point, related_name='circ_ip1', on_delete=models.SET_NULL, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='circ_ip2', on_delete=models.SET_NULL, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='circ_cust', on_delete=models.SET_NULL, blank=True, null=True)
	id_object = models.ManyToManyField(Object, related_name='circ_obj', blank=True)

	created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	history = HistoricalRecords(related_name='history_circuit_log')

	trassa = models.ForeignKey("CircuitTransit", on_delete=models.SET_NULL, related_name="circuits", null=True)

	is_modified = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Канал для Формы 5.3'
		verbose_name_plural = 'Каналы для Формы 5.3'
		ordering = ('id',)

	def __str__(self):
		return self.name


class CircuitTransit(models.Model):
	trassa = SortedManyToManyField(Circuit, related_name="transits", blank=True)
	obj_trassa = models.ForeignKey(Transit, related_name="circuit_transit", on_delete=models.CASCADE, blank=True, null=True)
	reverse_circuits = models.CharField(max_length=350, blank=True, null=True)

	class Meta:
		verbose_name = 'Транзит'
		verbose_name_plural = 'Транзиты'
