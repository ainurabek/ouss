from .models import Object, Trassa
from django.dispatch import receiver
from django.db.models.signals import post_save



@receiver(post_save, sender=Object)
def create_track(sender, instance, created, update_fields, **kwargs):
	if created or not created:
		ip1 = str(instance.point1)
		name = str(instance.name)
		ip2 = str(instance.point2)
		type_of_trakt = str(instance.type_of_trakt)


		if type_of_trakt == 'ПГ':
			pg = str(instance.type_of_trakt)
			track = '('+ip1+')'+name+'('+ip2+','+pg+')' 
		else:
			track = '('+ip1+')'+name+'('+ip2+')'

		id_transit1 = instance.id_transit1
		id_transit2 = instance.id_transit2

		while id_transit1 != None or id_transit2 != None:
			if id_transit1 != None:
				if instance.id_object == id_transit1.id_transit2.id_object:
					if ip1 == str(id_transit1.point2):
						track = '(' + str(id_transit1.point1) + ')' + str(id_transit1.name) + 'x' + track
						break
					else:	
						track = '(' + str(id_transit1.point1) + ')' + str(id_transit1.name) + str(id_transit1.point2) + track
						break
				track = str(id_transit1.trassa) + track
				id_transit1 = id_transit1.id_transit1
			if id_transit2 != None:

				if instance.id_object == id_transit2.id_transit1.id_object:
					if ip2 == str(id_transit2.point1):
						track = track + 'x' + str(id_transit2.name) + '(' +str(id_transit2.point2) + ')'
						break
					else:
						track = track + str(id_transit2.point1) + str(id_transit2.name) + '(' +str(id_transit2.point2) + ')'
						break
				track = track + str(id_transit2.trassa)
				id_transit2 = id_transit2.id_transit2
		trasa_pk = instance.trasa

		if trasa_pk == None:
			trasa = Trassa.objects.create(name=track)
			sender.objects.filter(pk=instance.pk).update(trassa=trassa.pk)
		else:
			trasa = Trassa.objects.filter(pk=instance.trassa.pk).update(name=track)