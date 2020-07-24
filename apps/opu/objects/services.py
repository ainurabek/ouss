from apps.opu.objects.models import TypeOfTrakt


def check_parent_type_of_trakt(parent):
    return True if parent.type_of_trakt is not None else False

def get_parent_type_of_trakt(parent_obj):
    if check_parent_type_of_trakt(parent=parent_obj):
        return TypeOfTrakt.objects.get(pk=parent_obj.type_of_trakt.pk)
    return False


def get_type_of_trakt(parent_obj):
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
        return type_obj
    return None


def create_circuit(model, obj, request):
    amount_channels = int(request.data['amount_channels'])
    if amount_channels == 12 or amount_channels == 30:
        for num_cir in range(1, amount_channels+1):
            model.objects.create(name=obj.name + '/' + str(num_cir),
                                   id_object=obj,
                                   num_circuit=num_cir,
                                   category=obj.category,
                                   point1=obj.point1,
                                   point2=obj.point2,
                                   created_by=request.user.profile)


def save_old_object(obj):
    obj_name = str(obj.name)
    obj_point1 = str(obj.point1)
    obj_point2 = str(obj.point2)
    return obj_name, obj_point1, obj_point2

def update_circuit(model, old_obj, obj):
    obj_name, obj_point1, obj_point2 = old_obj
    if obj_name != obj.name:
        circuits = model.objects.filter(id_object=obj)
        all = model.objects.filter(id_object=obj).count() + 1
        cir = 1
        for circuit in circuits:
            if cir <= all:
                circuit.name = model.objects.filter(pk=circuit.id).update(name=obj.name + "/" + str(cir))
                cir += 1

    if obj_point1 != obj.point1 or obj_point2 != obj.point2:
        circuits = model.objects.filter(id_object=obj.id)
        all = model.objects.filter(id_object=obj.id).count() + 1

        for circuit in circuits:
            all -= 1
            circuit.name = model.objects.filter(pk=circuit.id).update(
                point1=obj.point1.id,
                point2=obj.point2.id)