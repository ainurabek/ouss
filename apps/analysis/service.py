
from datetime import datetime




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

def changed_fields(obj, instance):
    all = obj.history.all()
    exact_history = all.first()
    print(exact_history.history_id)
    history = ""
    for h in all:
        #все предыдущие истории перед последним, у последнего нет
        if h.prev_record:
            delta = h.diff_against(h.prev_record) # сравнивается все истории с предыдущими историями

            for change in delta.changes:
                history = " {} изменился от {} к {}".format(change.field, change.old, change.new)
            print(history)
    exact_history.changed_field = history
    exact_history.save()













