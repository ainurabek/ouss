from apps.opu.objects.models import TypeOfTrakt, Object, Point

from apps.opu.form51.models import Form51

from apps.analysis.models import AmountChannelsKLSRRL

from apps.logging.form51.views import Form51LogUtil


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
        circuits = obj.circuit_object_parent.all()
        for circuit in circuits:
            circuit.name = obj.name + "/" + circuit.num_circuit
            circuit.save()

    if obj_point1 != obj.point1.point or obj_point2 != obj.point2.point:
        for circuit in obj.circuit_object_parent.all():
            circuit.point1 = obj.point1
            circuit.point2 = obj.point2
            circuit.save()


def get_count_active_channels(instance: Object):
    count = 0

    for obj in instance.parents.all():
        count += obj.total_amount_channels
    return count


def update_total_amount_channels(instance: Object):
    id_parent_instance = instance.id_parent
    while True:
        if id_parent_instance.id_parent is None:
            id_parent_instance.total_amount_channels = 0
            id_parent_instance.save()
            id_parent_instance.total_amount_channels = get_count_active_channels(id_parent_instance)
            id_parent_instance.save()
            break
        id_parent_instance.total_amount_channels = 0
        id_parent_instance.save()
        id_parent_instance.total_amount_channels = get_count_active_channels(id_parent_instance)
        id_parent_instance.save()
        id_parent_instance = id_parent_instance.id_parent


def create_form51(obj:Object):
    instance = Form51.objects.create(object = obj, customer = obj.customer, created_by = obj.created_by)
    Form51LogUtil(instance.created_by.user, instance.pk).form51_create_action('form51_created')


def create_object_KLSS_RRL_amount_channels(obj: Object):
    AmountChannelsKLSRRL.objects.create(object=obj)


def create_point_KLSS_RRL_amount_channels(ips: Point):
    AmountChannelsKLSRRL.objects.create(ips=ips)


def check_circuit_transit(trassa):
    for obj in trassa:
        if obj.circuit_object_parent.filter(is_modified=True).exists():
            return False
    return True
