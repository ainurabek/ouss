
from django.utils.safestring import mark_safe
from django import template

from apps.opu.objects.models import TPO, Outfit,Point, Category, LineType, TypeOfTrakt, Object, TypeOfLocation

from apps.opu.customer.models import Customer

register = template.Library()
from django.db.models import Q

@register.simple_tag
def get_customer_diff(history):
    message = ''
    old_record = history.instance.history_customer_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)