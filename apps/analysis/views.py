from django.views.generic import DetailView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
import datetime

from apps.analysis.serializers import DispEvent1ListSerializer, HistoryEventSerializer
from django.http import JsonResponse

from apps.analysis.service import get_period, get_type_line, get_calls_list, get_amount_of_channels, changed_fields
from apps.dispatching.models import Event
from apps.dispatching.services import get_event_name
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter



def get_report(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.get("responsible_outfit")

    all_event = Event.objects.filter(index1_id=3, callsorevent=False)

    if responsible_outfit != "":
        all_event = all_event.filter(responsible_outfit_id=responsible_outfit)

    if date_from != "" and date_to == "":
        all_event = all_event.filter(created_at=date_from)
    elif date_from == "" and date_to != "":
        all_event = all_event.filter(created_at=date_to)
    elif date_from != "" and date_to != "":
        all_event = all_event.filter(created_at__gte=date_from, created_at__lte=date_to)

    all_event_name = all_event.order_by("ips_id", "object_id", "circuit_id").distinct("ips_id", "object_id", "circuit_id")
    print(all_event_name)
    outfits = all_event.order_by("responsible_outfit").distinct("responsible_outfit")


    data = []
    for outfit in outfits:
        total_outfit = {"name1": 0, "name2": 0, "name3": 0, "name4": 0, 'name5':0, 'name6':0, 'name7':0, 'name8':0 }
        data.append({
            "name": outfit.responsible_outfit.outfit,
            "date_from": None, "comments": None,
            "reason": None, "type_line": None, "color":'1',
            "period_of_time": {"name1": None, "name2": None, "name3": None,
                               "name4": None, "name5":None, "name6":None, 'name7':None, 'name8':None }, "amount_of_channels": None
        })
        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            data.append({
                "name": get_event_name(event),
                "date_from": None, "comments": None,
                "reason": None, "type_line": None,
                "period_of_time": {"name1": None, "name2": None, "name3": None,
                                   "name4": None, "name5":None, "name6":None, 'name7':None, 'name8':None },
                "amount_of_channels": None
            })
            total_period_of_time = {"name1": 0, "name2": 0, "name3": 0, "name4": 0,
                                    'name5':0, 'name6':0, 'name7':0, 'name8':0}


            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                type_line = get_type_line(call)
                amount_of_channels = get_amount_of_channels(call)
                period_reason = {"name1": None, "name2": None, "name3": None, "name4": None,
                                 "name5":None, "name6":None, "name7":None, "name8":None}
                if call.reason.id == 1 and type_line == 1:
                    total_period_of_time["name1"] += period
                    period_reason["name1"] = period
                elif call.reason.id ==1 and type_line ==2:
                    total_period_of_time["name2"] += period
                    period_reason["name2"] = period
                elif call.reason.id == 2 and type_line==1:
                    total_period_of_time["name3"] += period
                    period_reason["name3"] = period
                elif call.reason.id == 2 and type_line==2:
                    total_period_of_time["name4"] += period
                    period_reason["name4"] = period
                elif call.reason.id == 3 and type_line == 1:
                    total_period_of_time["name5"] += period
                    period_reason["name5"] = period
                elif call.reason.id == 3 and type_line == 2:
                    total_period_of_time["name6"] += period
                    period_reason["name6"] = period
                elif call.reason.id == 4 and type_line ==1:
                    total_period_of_time["name7"] += period
                    period_reason["name7"] = period
                elif call.reason.id == 4 and type_line ==2:
                    total_period_of_time["name8"] += period
                    period_reason["name8"] = period

                data.append({
                    "name": None, "date_from": call.date_from,
                    "date_to": call.date_to, "comments": call.comments1,
                    "reason": call.reason.id, "type_line": type_line,
                    "period_of_time": period_reason, "amount_of_channels": amount_of_channels
                })

            total = dict(total_period_of_time)
            for i in total:
                total[i] = total[i] * int(get_amount_of_channels(event))
                total_outfit[i] += total[i]
            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "period_of_time": total_period_of_time, "color":'2'
            })

            data.append({
                "name": "всего", "date_from": "кнл/час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "period_of_time": total, "color":'3'
            })

        data.append({
            "name": "Общий итог", "date_from": None, "comments": None,
            "reason": None, "type_line": None,
            "period_of_time": total_outfit, "color":'4'
        })

    return JsonResponse(data, safe=False)


class DispEvent1ListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=False, index1__id=3)
    lookup_field = 'pk'
    serializer_class = DispEvent1ListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('object', 'ips', 'circuit', 'responsible_outfit',)

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.queryset.filter(created_at=today)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_to == "" and date_from != '':
            queryset = self.queryset.filter(created_at=date_from)
        elif date_to != '' and date_from == '':
            queryset = self.queryset.filter(created_at=date_to)
        elif date_to != '' and date_from != '':
            queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to)

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
        history = event.history.all()
        serializer = HistoryEventSerializer(history, many=True)
        changed_fields(obj=event, instance=history)
        return Response(serializer.data, status=status.HTTP_200_OK)


        # event = Event.objects.get(pk=pk)
        # histories = event.history.all()
        # print(histories)
        # for h in histories:
        #     if h.prev_record:
        #         delta = h.diff_against(h.prev_record)
        #
        #         b = ''
        #         for change in delta.changes:
        #             text = ("{} изменился от {} к {};".format(change.field, change.old, change.new))
        #             b += text
        #             a = {}
        #             data = []
        #             a['id'] = h.history_id
        #             a['date'] = h.history_date
        #             a['user'] = f"{h.history_user.first_name} {h.history_user.last_name}"
        #             a['type'] = h.history_type
        #             a['changed_field'] = b
        #             data.append(a)
        #             return Response(data, status=status.HTTP_200_OK)
        #     if h.history_type == '+':
        #         return Response("Создан обьект:{} Дата:{} Кем:{}".format(h.instance, h.history_date, h.history_user))
        #     elif h.history_type == '-':
        #         return Response("Удален обьект:{} Дата:{} Кем:{}".format(h.instance, h.history_date, h.history_user))

