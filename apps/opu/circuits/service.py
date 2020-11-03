
from django.utils.safestring import mark_safe
from django import template

from apps.opu.objects.models import TPO, Outfit,Point, Category, LineType, TypeOfTrakt, Object, \
    TypeOfLocation, InOut

from apps.opu.customer.models import Customer

from apps.opu.circuits.models import Measure, Mode, TypeCom


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
            elif "in_out" == change.field:
                old = InOut.objects.get(pk=change.old)
                new = InOut.objects.get(pk=change.new)
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