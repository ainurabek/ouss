from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
import datetime

from apps.analysis.serializers import DispEvent1ListSerializer, HistoryEventSerializer
from django.http import JsonResponse, HttpResponse

from apps.analysis.service import get_period, get_type_line, get_calls_list, get_amount_of_channels
from apps.dispatching.models import Event, HistoricalEvent
from apps.dispatching.services import get_event_name
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


def get_report(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.get("responsible_outfit")
    all_event = Event.objects.filter(index1_id=6, callsorevent=False)

    if responsible_outfit != "":
        all_event = all_event.filter(responsible_outfit_id=responsible_outfit)

    if date_from != "" and date_to == "":
        all_event = all_event.filter(created_at=date_from)
    elif date_from == "" and date_to != "":
        all_event = all_event.filter(created_at=date_to)
    elif date_from != "" and date_to != "":
        all_event = all_event.filter(created_at__gte=date_from, created_at__lte=date_to)

    all_event_name = all_event.order_by("ips_id", "object_id", "circuit_id").distinct("ips_id", "object_id", "circuit_id")

    outfits = all_event.order_by("responsible_outfit").distinct("responsible_outfit")

    data = []
    for outfit in outfits:
        total_outfit = {"1": 0, "2": 0, "3": 0, "4": 0}
        data.append({
            "name": outfit.responsible_outfit.outfit,
            "date_from": None, "comments": None,
            "reason": None, "type_line": None,
            "period_of_time": None, "amount_of_channels": None
        })
        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            data.append({
                "name": get_event_name(event),
                "date_from": None, "comments": None,
                "reason": None, "type_line": None,
                "period_of_time": None, "amount_of_channels": None
            })
            total_period_of_time = {"1": 0, "2": 0, "3": 0, "4": 0}

            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                type_line = get_type_line(call)
                amount_of_channels = get_amount_of_channels(call)
                if call.reason.id == 1:
                    total_period_of_time["1"] += period
                elif call.reason.id == 2:
                    total_period_of_time["2"] += period

                data.append({
                    "name": None, "date_from": call.date_from,
                    "date_to": call.date_to, "comments": call.comments1,
                    "reason": call.reason.id, "type_line": type_line,
                    "period_of_time": period, "amount_of_channels": amount_of_channels
                })

            total = dict(total_period_of_time)
            for i in total:
                total[i] = total[i] * int(get_amount_of_channels(event))
                total_outfit[i] += total[i]
            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "total_hours": total_period_of_time
            })

            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "total_channel_in_hours": total
            })

        data.append({
            "name": "всего", "date_from": "час", "comments": None,
            "reason": None, "type_line": get_type_line(event),
            "total_outfit": total_outfit
        })

    return JsonResponse(data, safe=False)


class DispEvent1ListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=True)
    lookup_field = 'pk'
    serializer_class = DispEvent1ListSerializer

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.queryset.filter(created_at=today,  index1__id=8, callsorevent=False)

        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if responsible_outfit is not None and responsible_outfit != '':
            queryset = self.queryset.filter(responsible_outfit=responsible_outfit, index1__id=8)
        if date_to == "" and date_from != '':
            queryset = self.queryset.filter(created_at=date_from, index1__id=8)
        elif date_to != '' and date_from == '':
            queryset = self.queryset.filter(created_at=date_to, index1__id=8)
        elif date_to != '' and date_from != '':
            queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to, index1__id=8)

        return queryset

# class DispEventHistory(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     authentication_classes = (TokenAuthentication,)
#     queryset = HistoricalEvent.objects.all()
#     lookup_field = 'pk'
#     serializer_class = HistoryEventSerializer

class DispEventHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        history = HistoricalEvent.objects.filter(id=event.pk)
        serializer = HistoryEventSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)