from django.db import models

# Create your models here.

class TraktOrLine(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name


class InOut(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name


class Measure(models.Model):
	index = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.name}, {self.index}'


class Speed(models.Model):
	index = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name


class TPO(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	tpo = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.name}, {self.tpo}'


class TypeOfTrakt(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	group = models.CharField(max_length=100, blank=True, null=True)
	
	def __str__(self):
		return self.name
class Type(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	_id = models.CharField(max_length=100, blank=True, null=True)
	
	def __str__(self):
		return f'{self.name}, {self._id}'


class TypeOfLocation(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)	
	
	def __str__(self):
		return self.name

class Customer(models.Model):
	id_customer = models.CharField(max_length=100, blank=True, null=True)
	customer = models.CharField(max_length=250, blank=True, null=True)
	abr = models.CharField(max_length=100, blank=True, null=True)
	address = models.CharField(max_length=250, blank=True, null=True)
	email = models.EmailField(max_length=250, blank=True, null=True)
	adding = models.CharField(max_length=200, blank=True, null=True)
	reuisits = models.CharField(max_length=200, blank=True, null=True)
	our_services_to = models.CharField(max_length=200, blank=True, null=True)
	connection_points = models.CharField(max_length=200, blank=True, null=True)
	date =  models.DateField()
	
	def __str__(self):
		return self.abr	

class Phone(models.Model):
	id_PP = models.CharField(max_length=100, blank=True, null=True)
	person = models.CharField(max_length=200, blank=True, null=True)
	id_customer = models.ForeignKey(Customer, related_name='phone_cust', on_delete=models.CASCADE, blank=True, null=True)
	phone_or_fax = models.CharField(max_length=100, blank=True, null=True)

class LineType(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	_id = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.name}, {self._id}'

class Mode(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	_id = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	_id = models.CharField(max_length=100, blank=True, null=True)
	
	def __str__(self):
		return self._id

class System(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True)
	_id = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name	

class Outfit(models.Model):
	id_outfit = models.CharField(max_length=100, blank=True, null=True)
	outfit = models.CharField(max_length=100, blank=True, null=True)
	adding = models.CharField(max_length=100, blank=True, null=True)
	num_outfit = models.CharField(max_length=100, blank=True, null=True)
	tpo = models.ForeignKey(TPO, related_name='out_tpo', on_delete=models.CASCADE, blank=True, null=True)
	type_outfit = models.ForeignKey(TypeOfLocation, related_name='out_tpo', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.outfit

class Point(models.Model):
	point = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	id_outfit = models.ForeignKey(Outfit, related_name='point_out', on_delete=models.CASCADE, blank=True, null=True)
	tpo = models.ForeignKey(TPO, related_name='point_tpo', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.point


class Trasa(models.Model):
	name = models.CharField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return self.name

class Object(models.Model):
	'''Линии Передачи, Тракт , ВГ-ПГ'''
	trasa = models.ForeignKey(Trasa, related_name='object_trasa', on_delete=models.CASCADE, blank=True, null=True)
	id_object = models.CharField(max_length=100, blank=True, null=True)
	id_parent = models.ForeignKey('Object', on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	COreceive = models.CharField(max_length=100, blank=True, null=True)
	COdeliver = models.CharField(max_length=100, blank=True, null=True)
	inter_code = models.CharField(max_length=100, blank=True, null=True)
	id_outfit = models.ForeignKey(Outfit, related_name='obj_out',on_delete=models.CASCADE, blank=True, null=True)
	tpo1 = models.ForeignKey(TPO, related_name='obj_tpo', on_delete=models.CASCADE, blank=True, null=True)
	point1 = models.ForeignKey(Point, related_name='obj_point', on_delete=models.CASCADE, blank=True, null=True)
	tpo2 = models.ForeignKey(TPO, related_name='obj_tpo2', on_delete=models.CASCADE, blank=True, null=True)
	point2 = models.ForeignKey(Point, related_name='obj_point2', on_delete=models.CASCADE, blank=True, null=True)
	category = models.ForeignKey(Category, related_name='obj_category', on_delete=models.CASCADE, blank=True, null=True)
	trakt = models.ForeignKey(TraktOrLine, related_name='obj_trakt', on_delete=models.CASCADE, blank=True, null=True)
	num = models.CharField(max_length=100, blank=True, null=True)
	system = models.ForeignKey(System, related_name='obj_system', on_delete=models.CASCADE, blank=True, null=True)
	main = models.BooleanField()
	_complex = models.BooleanField()
	type_transit1 = models.CharField(max_length=100, blank=True, null=True)
	type_transit2 = models.CharField(max_length=100, blank=True, null=True)
	id_transit1 = models.ForeignKey('Object', related_name='transit_obj', on_delete=models.CASCADE, blank=True, null=True)
	id_transit2 = models.ForeignKey('Object', related_name='transit2_obj', on_delete=models.CASCADE, blank=True, null=True)
	comments = models.CharField(max_length=100, blank=True, null=True)
	handel_add_path1 = models.CharField(max_length=100, blank=True, null=True)
	handel_add_path2 = models.CharField(max_length=100, blank=True, null=True)
	destination1 = models.ForeignKey('IP', related_name='obj_dest1', on_delete=models.CASCADE, blank=True, null=True)
	destination2 = models.ForeignKey('IP', related_name='obj_dest2', on_delete=models.CASCADE, blank=True, null=True)
	our = models.ForeignKey(TypeOfLocation, related_name='obj_our', on_delete=models.CASCADE, blank=True, null=True)
	amount_chenals = models.CharField(max_length=100, blank=True, null=True)
	not_in_use = models.BooleanField()
	type_line = models.ForeignKey(LineType, related_name='obj_type_line',on_delete=models.CASCADE, blank=True, null=True)
	num_optic_fiber = models.CharField(max_length=100, blank=True, null=True)
	type_of_trakt = models.ForeignKey(TypeOfTrakt, related_name='obj_trakt_type', on_delete=models.CASCADE, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='obj_cust', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.id_object}, {self.name}'



class IP(models.Model):
	point_id = models.ForeignKey(Point, on_delete=models.CASCADE, blank=True, null=True)
	object_id = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
	tpo_id = models.ForeignKey(TPO, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.point_id.point


class SubsRoutes(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	route = models.CharField(max_length=100, blank=True, null=True)

class Circuit(models.Model):
	"""Каналы"""
	id_circuit = models.CharField(max_length=100, blank=True, null=True)
	num_circuit = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	type_using = models.CharField(max_length=100, blank=True, null=True)#######
	category = models.ForeignKey(Category, related_name='circ_category', on_delete=models.CASCADE, blank=True, null=True) ###
	num_order = models.CharField(max_length=100, blank=True, null=True)
	date_order = models.CharField(max_length=100, blank=True, null=True)
	num_arenda = models.CharField(max_length=100, blank=True, null=True)
	number = models.ForeignKey(Phone, related_name='circ_phone', on_delete=models.CASCADE, blank=True, null=True)
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

class Circuit1(models.Model):
	id_circuit = models.CharField(max_length=100, blank=True, null=True)
	num_circuit = models.CharField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	type_using = models.CharField(max_length=100, blank=True, null=True)#######
	category = models.ForeignKey(Category, related_name='circ1_category', on_delete=models.CASCADE, blank=True, null=True) ###
	num_order = models.CharField(max_length=100, blank=True, null=True)
	date_order = models.CharField(max_length=100, blank=True, null=True)
	num_arenda = models.CharField(max_length=100, blank=True, null=True)
	number = models.ForeignKey(Phone, related_name='circ1_phone', on_delete=models.CASCADE, blank=True, null=True)
	speed = models.ForeignKey(Speed, related_name='circ1_speed', on_delete=models.CASCADE, blank=True, null=True)
	measure = models.ForeignKey(Measure, related_name='circ1_measure', on_delete=models.CASCADE, blank=True, null=True)
	adding = models.CharField(max_length=100, blank=True, null=True)
	comments = models.CharField(max_length=100, blank=True, null=True)
	type_transit1 = models.CharField(max_length=100, blank=True, null=True)
	type_transit2 = models.CharField(max_length=100, blank=True, null=True)
	id_transit1 = models.CharField(max_length=100, blank=True, null=True)
	id_transit2 = models.CharField(max_length=100, blank=True, null=True)
	in_out = models.ForeignKey(InOut, related_name='circ1_in', on_delete=models.CASCADE, blank=True, null=True)
	first = models.BooleanField()
	handel_add_path1 = models.CharField(max_length=100, blank=True, null=True)
	handel_add_path2 = models.CharField(max_length=100, blank=True, null=True)
	destination1 = models.ForeignKey(IP, related_name='circ1_ip1', on_delete=models.CASCADE, blank=True, null=True)
	destination2 = models.ForeignKey(IP, related_name='circ1_ip2', on_delete=models.CASCADE, blank=True, null=True)
	customer = models.ForeignKey(Customer, related_name='circ1_cust', on_delete=models.CASCADE, blank=True, null=True)
	id_object = models.ForeignKey(Object, related_name='circ1_obj', on_delete=models.CASCADE, blank=True, null=True)
	mode = models.ForeignKey(Mode, related_name='circ1_mode', on_delete=models.CASCADE, blank=True, null=True)
	type_com = models.ForeignKey(Type, related_name='circ1_type_com', on_delete=models.CASCADE, blank=True, null=True)
	id_subst =  models.ForeignKey(SubsRoutes, related_name='circ1_subst', on_delete=models.CASCADE, blank=True, null=True)


class TransitObject(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	id_complex_object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
	id_object = models.ForeignKey(Object1, on_delete=models.CASCADE, blank=True, null=True)
	num = models.CharField(max_length=100, blank=True, null=True)


class Bypass(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	num = models.CharField(max_length=100, blank=True, null=True)
	num_p = models.CharField(max_length=100, blank=True, null=True)
	id_main = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True)
	id_bypass = models.ForeignKey(Circuit1, on_delete=models.CASCADE, blank=True, null=True)


class AssignPart(models.Model):
	_id = models.CharField(max_length=100, blank=True, null=True)
	id_object_main =  models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
	id_object_part =  models.ForeignKey(Object1, on_delete=models.CASCADE, blank=True, null=True)


