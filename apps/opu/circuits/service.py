
from django.utils.safestring import mark_safe
from django import template

from apps.opu.objects.models import TPO, Outfit,Point, Category, LineType, TypeOfTrakt, Object, \
    TypeOfLocation

from apps.opu.customer.models import Customer

from apps.opu.circuits.models import Measure, Mode, TypeCom

from apps.opu.circuits.models import Circuit

from apps.opu.objects.services import update_total_amount_channels

register = template.Library()
from django.db.models import Q

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
            elif "measure" == change.field:
                old = Measure.objects.get(pk=change.old)
                new = Measure.objects.get(pk=change.new)
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
            elif "mode"  == change.field:
                old = Mode.objects.get(pk=change.old)
                new = Mode.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "type_com"  == change.field:
                old = TypeCom.objects.get(pk=change.old)
                new = TypeCom.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)

def create_circuit(obj: Object, request):
    active = int(request.data['active'])
    if int(request.data['create_circuit']):
        for num_cir in range(1, obj.amount_channels.value+1):
            c = Circuit.objects.create(name=obj.name + '/' + str(num_cir), num_circuit=num_cir,
                                 category=obj.category, point1=obj.point1, point2=obj.point2,
                                 created_by=request.user.profile, first=active, object=obj)
            c.id_object.add(obj)
            c.transit.add(c)
        #чтобы добавлять каналы в список всех каналов id_parent
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

