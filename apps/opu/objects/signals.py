from .models import Object, TypeOfTrakt
from django.dispatch import receiver
from django.db.models.signals import pre_save



@receiver(pre_save, sender=Object)
def create_track(sender, instance, *args, **kwargs):
	# if created :

	if instance.id_parent != None and instance.id_parent.type_of_trakt != None:
		if instance.id_parent.type_of_trakt.name == 'ВГ':
			type_obj = TypeOfTrakt.objects.get(name='ПГ')
			sender.objects.filter(pk=instance.pk).update(type_of_trakt=type_obj)
		elif instance.id_parent.type_of_trakt.name == 'ТГ':
			type_obj = TypeOfTrakt.objects.get(name='ВГ')
			sender.objects.filter(pk=instance.pk).update(type_of_trakt=type_obj)
		elif instance.id_parent.type_of_trakt.name == 'ЧГ':
			type_obj = TypeOfTrakt.objects.get(name='ТГ')
			sender.objects.filter(pk=instance.pk).update(type_of_trakt=type_obj)
		elif instance.id_parent.type_of_trakt.name == 'РГ':
			type_obj = TypeOfTrakt.objects.get(name='ЧГ')
			sender.objects.filter(pk=instance.pk).update(type_of_trakt=type_obj)


