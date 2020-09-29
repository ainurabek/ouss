
from datetime import datetime
from django import template
register = template.Library()
from django.db.models import Q
from django.utils.safestring import mark_safe



def get_period(obj, date_to):
    if obj.date_to != None and obj.date_from != None:
        date = (obj.date_to) - (obj.date_from)
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time

    if obj.date_to == None:
        if date_to is not None and date_to != "":
            date_to = datetime.fromisoformat(date_to + "T23:59:59")
            date = date_to - obj.date_from
            period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
            return period_of_time
        date = datetime.now()
        newdate = date.replace(hour=23, minute=59, second=59)
        date = newdate - obj.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time


def get_type_line(obj):
    if obj.object is not None:
        return obj.object.type_line.main_line_type.id
    elif obj.circuit is not None:
        return obj.circuit.id_object.type_line.main_line_type.id
    elif obj.ips is not None:
        return obj.ips.object_id.type_line.main_line_type.id


def get_calls_list(all_event, obj):
    if obj.object is not None:
        print(obj)
        print(all_event)
        return all_event.filter(object=obj.object)
    elif obj.ips is not None:
        return all_event.filter(ips=obj.ips)
    elif obj.circuit is not None:
        return all_event.filter(circuit=obj.circuit)

def get_amount_of_channels(obj):
    if obj.object is not None:
        return obj.object.total_amount_active_channels
    elif obj.ips is not None:
        return obj.ips.object_id.total_amount_active_channels
    elif obj.circuit is not None:
        return obj.circuit.id_object.total_amount_active_channels


@register.simple_tag
def get_diff(history):
    message = ''
    old_record = history.instance.history_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()

    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)















