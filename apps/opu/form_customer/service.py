from django.utils.safestring import mark_safe
from django import template

from apps.opu.objects.models import TPO, Outfit,Point, Category, LineType, TypeOfTrakt, Object, TypeOfLocation

from apps.opu.customer.models import Customer

from apps.opu.circuits.models import Circuit

register = template.Library()
from django.db.models import Q

@register.simple_tag
def get_form_customer_diff(history):
    message = ''
    old_record = history.instance.history_form_customer_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "customer" == change.field:
                old = Customer.objects.get(pk=change.old)
                new = Customer.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "object" == change.field:
                old_tpo = Object.objects.get(pk=change.old)
                new_tpo = Object.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_tpo, new_tpo)
            elif "circuit" == change.field:
                old = Circuit.objects.get(pk=change.old)
                new = Circuit.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)