import datetime
from datetime import timedelta
from rest_framework.generics import ListAPIView
from apps.dispatching.models import Event


class ListFilterAPIView(ListAPIView):

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if date_to == "" and date_from == "":
            week = datetime.date.today() - timedelta(days=7)
            queryset = self.queryset.filter(created_at__gte=week)

        else:

            if date_to == "" and date_from != '':
                queryset = self.queryset.filter(created_at=date_from)
            elif date_to != '' and date_from == '':
                queryset = self.queryset.filter(created_at=date_to)
            else:
                if date_to != '' and date_from != '':
                    queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to)

        return queryset


def get_minus_date(days: int):
    return datetime.date.today() - timedelta(days=days)


def get_event_name(event_object) -> str:

    event_name = None

    if event_object.object is not None:
        event_name = event_object.object.name
    elif event_object.ips is not None:
        event_name = event_object.ips.name
    elif event_object.circuit is not None:
        event_name = event_object.circuit.name
    else:
        event_name = event_object.name

    return event_name


def get_event(event_object) -> Event:
    event = None
    if event_object.object is not None:
        event = event_object.object
    elif event_object.ips is not None:
        event = event_object.ips
    elif event_object.circuit is not None:
        event = event_object.circuit
    elif event_object.name is not None:
        event = event_object
    return event

def get_date_to(obj: Event, created_at: str):
    data = None
    if obj.id_parent is not None:
        data = obj.id_parent.date_to
    if obj.date_to is not None:

        if str(obj.date_to.date()) != created_at:
            data = created_at + "T24:00:00"
        else:
            data = obj.date_to

    else:
        data = created_at + "T24:00:00"
    return data

