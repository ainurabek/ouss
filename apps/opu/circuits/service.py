from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django import template
from apps.opu.objects.models import Point, Category, Object, Transit
from apps.opu.customer.models import Customer
from apps.opu.circuits.models import Circuit, CircuitTransit
from apps.opu.objects.services import update_total_amount_channels
from django.db.models import Q, Count

register = template.Library()


@register.simple_tag
def get_circuit_diff(history):
    message = ''
    old_record = history.instance.history_circuit_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "category"  == change.field:
                old = Category.objects.get(pk=change.old)
                new = Category.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)

            elif "point1" == change.field:
                old = Point.objects.get(pk=change.old)
                new = Point.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "point2" == change.field:
                old = Point.objects.get(pk=change.old)
                new = Point.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "customer" == change.field:
                old = Customer.objects.get(pk=change.old)
                new = Customer.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "id_object"  == change.field:
                old = Object.objects.get(pk=change.old)
                new = Object.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)

            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)


def create_circuit(obj: Object, request):
    active = int(request.data['active'])
    if int(request.data['create_circuit']):
        for num_cir in range(1, obj.amount_channels.value+1):
            transit = CircuitTransit.objects.create()
            c = Circuit.objects.create(name=obj.name + '/' + str(num_cir), num_circuit=num_cir,
                                 category=Category.objects.get(index='6'), point1=obj.point1, point2=obj.point2,
                                 created_by=request.user.profile, first=active, object=obj, trassa=transit)
            transit.trassa.add(c)
            c.id_object.add(obj)

        #?????????? ?????????????????? ???????????? ?? ???????????? ???????? ?????????????? id_parent
        id_parent = obj.id_parent
        while True:
            if id_parent.id_parent is None:
                id_parent.circ_obj.add(*obj.circ_obj.all())
                id_parent.save()
                break
            id_parent.circ_obj.add(*obj.circ_obj.all())
            id_parent.save()
            id_parent = id_parent.id_parent
        update_circuit_active(object=obj)


def update_circuit_active(object: Object):
    # update_total_amount_channels(object)
    object.total_amount_channels = object.circuit_object_parent.filter(first=True).count()
    object.save()
    update_total_amount_channels(object)


def create_circuit_transit(object_transit: Transit):
    if object_transit.create_circuit_transit:
        max_count = object_transit.trassa.all().annotate(circuit_count=Count('circuit_object_parent')).order_by('-circuit_count').first()
        circuit_transits = {
            str(num): CircuitTransit.objects.create(obj_trassa=object_transit)
            for num in range(1, max_count.circuit_object_parent.count() + 1)
        }
        for key, transit in circuit_transits.items():
            for obj in object_transit.trassa.all().iterator():
                try:
                    circuit = obj.circuit_object_parent.get(num_circuit=key)
                    if circuit.trassa is not None:
                        circuit.trassa.delete()

                    circuit.trassa = transit
                    circuit.save()

                    transit.trassa.add(circuit)
                except ObjectDoesNotExist:
                    pass


def update_trassa_for_new_circuit(transit: CircuitTransit, circuits):
    for circuit in circuits:
        if not circuit.trassa:
            circuit.trassa = transit
            circuit.save()
        elif circuit.trassa != transit:
            circuit.trassa = transit
            circuit.save()


def create_new_trassa(circuits):
    prev = set()
    for circuit in circuits:
        if circuit not in prev:
            not_modified_circuit = circuit.object.circuit_object_parent.filter(is_modified=False).first()
            if not_modified_circuit and not_modified_circuit.trassa.obj_trassa != circuit.trassa.obj_trassa:
                circuit_transit = CircuitTransit.objects.create(obj_trassa=not_modified_circuit.trassa.obj_trassa)
                for obj in not_modified_circuit.trassa.obj_trassa.trassa.all().iterator():
                    try:
                        circuit = obj.circuit_object_parent.get(num_circuit=circuit.num_circuit)
                        circuit_transit.trassa.add(circuit)
                        circuit.trassa = circuit_transit
                        circuit.is_modified = False
                        circuit.save()
                        prev.add(circuit)
                    except ObjectDoesNotExist:
                        pass



def check_modified(transit: CircuitTransit):
    if set(circuit.object for circuit in transit.trassa.all()) == set(transit.obj_trassa.trassa.all()):
        for circuit in transit.trassa.all().iterator():
            circuit.is_modified = False
            circuit.save()
    else:
        for circuit in transit.trassa.all().iterator():
            circuit.is_modified = True
            circuit.save()
