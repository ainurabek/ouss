from apps.opu.circuits.models import Circuit
from apps.opu.objects.models import TypeOfTrakt, Object
from django.http import JsonResponse
from apps.opu.services import get_field_name_for_create_img


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
        elif type_of_trakt_parent.name == 'ПГ':
            type_obj = TypeOfTrakt.objects.get(name='ПГ')
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


def _update_object_total_amount_channels(object, flag, count):
    if flag:
        Object.objects.filter(pk=object.pk).update(total_amount_channels=int(object.total_amount_channels) + int(count))
    else:
        Object.objects.filter(pk=object.pk).update(total_amount_channels=int(object.total_amount_channels) - int(count))


def update_total_amount_channels(obj, flag=True):
    if obj.id_parent:
        count = obj.total_amount_channels
        while True:
            if obj.id_parent is None:
                _update_object_total_amount_channels(obj, flag, count)
                break
            if count == "" or count is None:
                break
            obj = Object.objects.get(pk=obj.id_parent.pk)
            if obj.total_amount_channels == "" or obj.total_amount_channels == None:
                break
            _update_object_total_amount_channels(obj, flag, count)


def get_active_channels(obj):
    active_channels = Circuit.objects.filter(first = True, id_object = obj).count()
    Object.objects.filter(pk=obj.pk).update(num = int(active_channels))

def get_total_amount_active_channels(instance):
    cir = instance.id_object
    while True:
        if instance.first:
            cir.total_amount_active_channels = int(cir.total_amount_active_channels) + 1
        else:
            cir.total_amount_active_channels = int(cir.total_amount_active_channels) - 1

        cir.save()

        if cir.id_parent is None:
            break
        else:
            cir = cir.id_parent
# def get_total_amount_active_channels(obj, instance):
#     cir = instance.id_object
#     while True:
#         if cir.id_parent is None:
#             if instance.first ==True:
#                 cir.total_amount_active_channels = int(cir.total_amount_active_channels)+1
#                 cir.save()
#             else:
#                 cir.total_amount_active_channels = int(cir.total_amount_active_channels) - 1
#                 cir.save()
#
#             break
#
#         if instance.first == True:
#             cir.total_amount_active_channels = int(cir.total_amount_active_channels) + 1
#             cir.save()
#             cir = cir.id_parent
#         else:
#
#             cir.total_amount_active_channels = int(cir.total_amount_active_channels) - 1
#             cir.save()
#             cir = cir.id_parent


def create_photo_for_object(model, model_photo, obj, field_name: str, request):
    img_field, obj_field = get_field_name_for_create_img(model, model_photo)
    for img in request.FILES.getlist(field_name):
        kwargs = {img_field: img}
        obj_photo = model_photo.objects.create(**kwargs)
        obj_photo.form53.add(obj)