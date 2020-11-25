from apps.opu.circuits.models import Circuit
from apps.opu.objects.models import TypeOfTrakt, Object

def check_parent_type_of_trakt(parent: Object):
    return True if parent.type_of_trakt is not None else False


def get_parent_type_of_trakt(parent_obj: Object):
    if check_parent_type_of_trakt(parent=parent_obj):
        return TypeOfTrakt.objects.get(pk=parent_obj.type_of_trakt.pk)
    return False


def get_type_of_trakt(parent_obj: Object):
    type_of_trakt_parent = get_parent_type_of_trakt(parent_obj)
    if type_of_trakt_parent:
        if type_of_trakt_parent.name == 'ВГ':
            type_obj = TypeOfTrakt.objects.get(name='ПГ')
        elif type_of_trakt_parent.name == 'ТГ':
            type_obj = TypeOfTrakt.objects.get(name='ВГ')
        elif type_of_trakt_parent.name == 'ЧГ':
            type_obj = TypeOfTrakt.objects.get(name='ТГ')
        elif type_of_trakt_parent.name == 'РГ':
            type_obj = TypeOfTrakt.objects.get(name='ЧГ')
        elif type_of_trakt_parent.name == 'ПГ':
            type_obj = TypeOfTrakt.objects.get(name='ПГ')
        return type_obj
    return None

def save_old_object(obj):
    obj_name = str(obj.name)
    obj_point1 = str(obj.point1)
    obj_point2 = str(obj.point2)
    return obj_name, obj_point1, obj_point2


def update_circuit(old_obj, obj: Object):
    obj_name, obj_point1, obj_point2 = old_obj
    if obj_name != obj.name:
        circuits = Circuit.objects.filter(id_object=obj)
        all = Circuit.objects.filter(id_object=obj).count() + 1
        cir = 1
        for circuit in circuits:
            if cir <= all:
                circuit.name = Circuit.objects.filter(pk=circuit.id).update(name=obj.name + "/" + str(cir))
                cir += 1

    if obj_point1 != obj.point1 or obj_point2 != obj.point2:
        circuits = Circuit.objects.filter(id_object=obj.id)

        for circuit in circuits:
            circuit.name = Circuit.objects.filter(pk=circuit.id).update(
                point1=obj.point1.id,
                point2=obj.point2.id)


def add_to_amount_channels(instance:Object, value, flag):
    if instance.parents.count() == 1:
        instance.total_amount_channels -= instance.total_amount_channels
        instance.save()
    if flag:
        instance.total_amount_channels += value
        instance.save()
    else:
        instance.total_amount_channels -= value
        instance.save()


def update_total_amount_channels(instance: Object, flag=True):
    value = instance.total_amount_channels
    id_parent_instance = instance.id_parent

    while True:
        if id_parent_instance.id_parent is None:
            add_to_amount_channels(id_parent_instance, value, flag)
            break
        add_to_amount_channels(id_parent_instance, value, flag)
        id_parent_instance = id_parent_instance.id_parent

def adding_an_object_to_trassa(obj: Object):
    obj.transit.add(obj)

