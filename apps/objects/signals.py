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
		trasa_pk = instance.trassa
		if trasa_pk == None:
			trasa = Trassa.objects.create(name=track)
			sender.objects.filter(pk=instance.pk).update(trassa=trasa.pk)
		else:
			trasa = Trassa.objects.filter(pk=instance.trassa.pk).update(name=track)