import datetime
import os
import pdfkit
import subprocess
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django_filters.rest_framework import DjangoFilterBackend
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TypeOfJournal, Comments, Reason, Index, Event
from .serializers import EventCreateSerializer, EventDetailSerializer
from .serializers import EventListSerializer, CommentsSerializer, TypeJournalSerializer, \
    ReasonSerializer, IndexSerializer, CallsCreateSerializer, DamageReportListSerializer, DamageUpdateSerializer, \
    InternationalDamageReportListSerializer, TechStopReportListSerializer
from .services import get_minus_date, ListFilterAPIView, get_event_name, \
    event_form_customer_filter_date_from_date_to_and_customer
from ..accounts.permissions import SuperUser, IsDispOnly, IngenerUser, DateCheck
from ..analysis.service import get_date_to_ak
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object, OutfitWorker, Outfit, Point
from ..opu.objects.serializers import OutfitWorkerListSerializer, OutfitWorkerCreateSerializer


class EventListAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=True).prefetch_related('object', 'circuit', 'ips', 'index1',
                                                                        'responsible_outfit')

    lookup_field = 'pk'
    serializer_class = EventListSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == "retrieve":
            return EventDetailSerializer

    def get_queryset(self):
        created_at = self.request.query_params.get('created_at', None)
        type_journal = self.request.query_params.get('type_journal', None)
        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        index1 = self.request.query_params.get('index1', None)
        name = self.request.query_params.get('name', None)
    # фильтр по хвостам + за сегодня

        queryset = self.queryset.filter(date_from__date__lte=created_at).order_by('-date_from')

    # фильтр  по дате создания, без времени + хвосты за предыдущие дни

        if type_journal is not None and type_journal != '':
            queryset = queryset.filter(type_journal=type_journal)
        if responsible_outfit is not None and responsible_outfit != '':
            queryset = queryset.filter(responsible_outfit=responsible_outfit)
        if index1 is not None and index1 != '':
            queryset = queryset.filter(index1=index1)
        if name is not None and name != '':
            queryset = queryset.filter(name=name)
        queryset = queryset.filter(Q(date_to__date=created_at) | Q(date_to__date=None) | Q(date_from__date=created_at)) \
                   |(queryset.exclude(index1__index='4', date_to__date__lt=created_at)
                      .filter(date_from__date__lt=created_at))
        return queryset

    def retrieve(self, request, pk=None, **kwargs):
        calls = Event.objects.get(pk=pk).event_id_parent.all().order_by("-date_from")

        serializer = self.get_serializer(calls, many=True)

        return Response(serializer.data)


class EventDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        created_at = request.GET.get("created_at")
        calls = get_object_or_404(Event, pk=pk).event_id_parent.filter(date_from__date__lte=created_at).order_by("-date_from")
        serializer = EventDetailSerializer(calls, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class EventIPCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)

    """Создания Event"""
    def post(self, request, pk):
        data = request.data
        point = Point.objects.get(pk=pk)
        created_events = Event.objects.filter(ips=point, callsorevent=True).exclude(index1__index='4')
        if created_events.exists():
            if data['create_new_call'] == False:
                message = {"detail": 'По такому ИПу уже существует событие'}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = EventCreateSerializer(data=request.data)
                if serializer.is_valid():
                    event = serializer.save(ips=point, created_by=self.request.user.profile)
                    Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                         time_created_at=event.time_created_at,
                                         date_from=event.date_from, index1=event.index1,
                                         type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                         reason=event.reason, comments1=event.comments1, ips=event.ips,
                                         responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                         customer=event.customer, created_by=event.created_by,
                                         contact_name=event.contact_name, )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(ips=point, created_by=self.request.user.profile)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 time_created_at=event.time_created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, ips=event.ips,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by,
                                 contact_name=event.contact_name,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointParentList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        point = Point.objects.get(pk=pk)
        created_events = Event.objects.filter(ips=point, callsorevent=True).exclude(index1__index='4')
        serializer = EventListSerializer(created_events, many=True).data
        return Response(serializer)


class ObjectParentList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        created_events = Event.objects.filter(object=obj, callsorevent=True).exclude(index1__index='4')
        serializer = EventListSerializer(created_events, many=True).data
        return Response(serializer)


class CircuitParentList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        created_events = Event.objects.filter(circuit=circuit, callsorevent=True).exclude(index1__index='4')
        serializer = EventListSerializer(created_events, many=True).data
        return Response(serializer)

class EventCircuitCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)

    """Создания Event"""

    def post(self, request, pk):
        data = request.data
        circuit = get_object_or_404(Circuit, pk=pk)
        created_events = Event.objects.filter(circuit=circuit, callsorevent=True).exclude(index1__index='4')
        if created_events.exists():
            if data['create_new_call'] == False:
                message = {"detail": 'По такому каналу уже существует событие'}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = EventCreateSerializer(data=request.data)
                if serializer.is_valid():
                    event = serializer.save(circuit=circuit, created_by=self.request.user.profile)
                    Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                         time_created_at=event.time_created_at,
                                         date_from=event.date_from, index1=event.index1,
                                         type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                         reason=event.reason, comments1=event.comments1, circuit=event.circuit,
                                         responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                         customer=event.customer, created_by=event.created_by,
                                         contact_name=event.contact_name,
                                         )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(circuit=circuit, created_by=self.request.user.profile)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 time_created_at=event.time_created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, circuit=event.circuit,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventObjectCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)
    """Создания Event"""

    def post(self, request, pk):
        data = request.data
        object = get_object_or_404(Object, pk=pk)
        created_events = Event.objects.filter(object=object, callsorevent=True).exclude(index1__index='4')
        if created_events.exists():
            if data['create_new_call'] == False:
                message = {"detail": 'По такому КО уже существует событие'}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = EventCreateSerializer(data=request.data)
                if serializer.is_valid():
                    event = serializer.save(object=object, created_by=self.request.user.profile)

                    Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                         time_created_at=event.time_created_at,
                                         date_from=event.date_from, index1=event.index1,
                                         type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                         reason=event.reason, comments1=event.comments1, object=event.object,
                                         responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                         customer=event.customer, created_by=event.created_by,
                                         contact_name=event.contact_name,
                                         )

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(object=object, created_by=self.request.user.profile)

            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 time_created_at=event.time_created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, object=event.object,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EventCallsCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser,)

    """Создания Event"""

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = CallsCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(id_parent=event, created_by=self.request.user.profile,
                                       callsorevent=False)
            all_calls = event.event_id_parent.all().order_by('-date_from')
            i = 0
            while i < (len(all_calls) -1):
                all_calls[i + 1].date_to = all_calls[i].date_from
                all_calls[i + 1].save()
                i += 1
            all_calls[0].date_to = None
            all_calls[0].save()
            instance.id_parent.date_from = all_calls.last().date_from
            instance.id_parent.date_to = all_calls[0].date_from
            instance.id_parent.index1 = all_calls[0].index1
            instance.id_parent.created_at = all_calls[0].created_at
            instance.id_parent.responsible_outfit = all_calls[0].responsible_outfit
            instance.id_parent.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdateAPIView(UpdateAPIView):
    """Редактирования event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)

    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    def perform_update(self, serializer):

        instance = serializer.save(created_by=self.request.user.profile)
        instance.id_parent.save()
        all_calls = instance.id_parent.event_id_parent.all().order_by('-date_from')
        i = 0
        while i < (len(all_calls) - 1):
            all_calls[i + 1].date_to = all_calls[i].date_from
            all_calls[i + 1].save()
            i += 1
        all_calls[0].date_to = None
        all_calls[0].save()
        instance.id_parent.date_from = all_calls.last().date_from
        instance.id_parent.date_to = all_calls[0].date_from
        instance.id_parent.index1 = all_calls[0].index1
        instance.id_parent.created_at = all_calls[0].created_at
        instance.id_parent.responsible_outfit = all_calls[0].responsible_outfit
        instance.id_parent.save()


class EventDeleteAPIView(DestroyAPIView):
    """Удаление события  по звонкам"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser, DateCheck)

    queryset = Event.objects.all()
    lookup_field = 'pk'

    def perform_destroy(self, instance):

        if instance.id_parent is None:
            instance.delete()
            return
        all_calls = instance.id_parent.event_id_parent.all().order_by('-date_from')
        instance.delete()
        i = 0
        if len(all_calls) >= 1:
            while i < (len(all_calls) - 1):
                all_calls[i + 1].date_to = all_calls[i].date_from
                all_calls[i + 1].save()
                i += 1
            all_calls[0].date_to = None
            all_calls[0].save()
            instance.id_parent.date_from = all_calls.last().date_from

            if len(all_calls) == 1:
                instance.id_parent.date_to = None
            else:
                instance.id_parent.date_to = all_calls[0].date_from
            instance.id_parent.index1 = all_calls[0].index1
            instance.id_parent.created_at = all_calls[0].created_at
            instance.id_parent.responsible_outfit = all_calls[0].responsible_outfit
            instance.id_parent.save()
        else:
            instance.id_parent.delete()


@permission_classes([IsAuthenticated,])
def get_dates_and_counts_week(request):
    """статистика событий за неделю"""
    data = {}
    dates = Event.objects.filter(date_from__date__gte=get_minus_date(days=7)).\
        exclude(callsorevent=False).order_by('date_from').distinct('date_from')


    teams_data = [
        {"day": date.date_from.strftime("%A"), "date": date.date_from.strftime("%Y-%m-%d"), "counts":Event.objects.filter(date_from__gte=date.date_from).exclude(callsorevent=False).count()}
        for date in dates
    ]
    data["dates"] = teams_data

    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated,])
def get_dates_and_counts_month(request):
    """статистика событий за месяц"""
    data = {}
    dates = Event.objects.filter(date_from__date__gte=get_minus_date(days=30)).\
        exclude(callsorevent=False).order_by('date_from').distinct('date_from')

    teams_data = [
        {"day": date.date_from.strftime("%A"), "date": date.date_from.strftime("%Y-%m-%d"), "counts": Event.objects.filter(date_from__gte=date.date_from).
            exclude(callsorevent=False).count() }
        for date in dates
    ]
    data["dates"] = teams_data

    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated,])
def get_dates_and_counts_today(request):
    """статистика событий за сегодня"""
    data = {}
    time = datetime.date.today()

    dates = Event.objects.filter(date_from__gte=time).\
        exclude(callsorevent=False).order_by('date_from').distinct('date_from')
    teams_data = [
        {"time": date.date_from, "counts": Event.objects.filter(date_from=date.date_from).exclude(callsorevent=False).count()}
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated, ])
def get_outfit_statistics_for_a_month(request):
    """статистика событий по предприятиям за месяц"""
    month = get_minus_date(days=30)
    dates = Event.objects.filter(date_from__date__gte=month).\
        exclude(callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, date_from__date__gte=month).
             exclude(callsorevent=False).count()}
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)

@permission_classes([IsAuthenticated,])
def get_outfit_statistics_for_a_week(request):
    """статистика событий по предприятиям за неделю"""
    week = get_minus_date(days=7)
    dates = Event.objects.filter(date_from__date__gte=week).exclude(callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, date_from__date__gte=week).
             exclude(callsorevent=False).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)

@permission_classes([IsAuthenticated,])
def get_outfit_statistics_for_a_day(request):
    """статистика событий по предприятиям за сегодня"""
    day = datetime.date.today()
    dates = Event.objects.filter(date_from__date__gte=day).\
        exclude(callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, date_from__date__gte=day).
             exclude(callsorevent=False).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


class CompletedEvents(ListFilterAPIView):
    """статистика событий по предприятиям за сегодня"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer
    queryset = Event.objects.filter(index1__index='4')


class UncompletedEventList(ListFilterAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer
    queryset = Event.objects.filter(date_to=None).exclude(callsorevent=False).exclude(index1__index='4')


@permission_classes([IsAuthenticated, ])
def get_report_object(request):
    date = request.GET.get("date")
    index = request.GET.get("index")

    all_events = Event.objects.filter(Q(date_to__date__gte=date) |Q(date_to__date = None), callsorevent=False).exclude(index1__index='4')
    all_events =all_events.filter(date_from__date__lte=date)

    if index is not None and index != "":
        all_events = all_events.filter(index1__id=index)

    all_event_names = all_events.order_by(
        "ips_id", "object_id", "circuit_id", "name", "responsible_outfit", "type_journal").distinct(
        "ips_id", "object_id", "circuit_id", "name", "responsible_outfit", "type_journal")

    type_journal = all_event_names.order_by("type_journal").distinct("type_journal")
    outfits = all_event_names.order_by("responsible_outfit", "type_journal").distinct("responsible_outfit", "type_journal")
    data = []

    for type in type_journal.iterator():
        data.append({"type_journal": type.type_journal.name,
                     "outfit": None,
                     "name": None,
                     "date_from": None,
                     "date_to": None,
                     "region": None,
                     "index1": None,
                     "reason": None,
                     "comments1": None})

        for out in outfits.filter(type_journal=type.type_journal).iterator():
            data.append({"outfit": out.responsible_outfit.outfit,
                     "name": None,
                     "type_journal": None,
                     "date_from": None,
                     "date_to": None,
                     "region": None,
                     "index1": None,
                     "reason": None,
                     "comments1": None})

            for event in all_event_names.filter(responsible_outfit=out.responsible_outfit,
                                                type_journal=type.type_journal).iterator():
                data.append({"outfit": None,
                             "name": get_event_name(event),
                             "type_journal": None,
                             "date_from": None,
                             "date_to": None,
                             "region": None,
                             "index1": None,
                             "reason": None,
                             "comments1": None})

                for call in all_events.filter(object=event.object, ips=event.ips, circuit=event.circuit,
                                              name=event.name, responsible_outfit=out.responsible_outfit,
                                              type_journal=type.type_journal).order_by('date_from').iterator():
                    data.append({"outfit": None,
                                 "name": '-',
                                 "type_journal": None,
                                 "date_from": call.date_from,
                                 "date_to": get_date_to_ak(call, date),
                                 "region": call.point1.name + " - " + call.point2.name if call.point1 is not None else "",
                                 "index1": call.index1.index,
                                 "reason": call.reason.name,
                                 "comments1": call.comments1})

    return JsonResponse(data, safe=False)

# @permission_classes([IsAuthenticated, ])
def get_report_pdf(request):
    date = request.GET.get("date")
    index = request.GET.get("index")
    all_events = Event.objects.filter(Q(date_to__date__gte=date) |Q(date_to__date = None), callsorevent=False).exclude(index1__index='4')
    all_events =all_events.filter(date_from__date__lte=date)

    if index is not None and index != "":
        all_events = all_events.filter(index1__id=index)

    all_event_names = all_events.order_by(
        "ips_id", "object_id", "circuit_id", "name", "responsible_outfit", "type_journal").distinct(
        "ips_id", "object_id", "circuit_id", "name", "responsible_outfit", "type_journal")

    type_journal = all_event_names.order_by("type_journal").distinct("type_journal")
    outfits = all_event_names.order_by("responsible_outfit", "type_journal").distinct("responsible_outfit", "type_journal")
    data = []
    all_tj = TypeOfJournal.objects.all().order_by("name").distinct("name")
    all_out = Outfit.objects.\
        defer('adding', 'num_outfit', 'tpo', 'type_outfit__name',
              'created_by', 'created_at', 'length_kls', 'length_vls',
              'length_rrl', 'total_number_kls', 'corresponding_norm_kls', 'total_number_vls', 'corresponding_norm_vls',
              'total_number_rrl', 'corresponding_norm_rrl').order_by("outfit").distinct("outfit")
    objs = Object.objects.defer('id_parent', 'id_outfit', 'category', 'point1', 'point2',
                  'type_of_trakt', 'tpo1', 'tpo2', 'comments', 'customer', 'type_line', 'our',
                  "ip_object",  'amount_channels', "total_amount_channels",'order_object_photo', 'consumer').order_by("name").distinct("name")
    ips = Point.objects.defer('point').order_by("name").distinct("name")
    cirs = Circuit.objects.defer('num_circuit', 'category', 'num_order', 'comments', 'trassa', 'first',
                  'point1', 'point2', 'customer', 'object').order_by("name").distinct("name")
    all_evs = all_events.defer('id', 'type_journal',  'date_from', 'date_to', 'contact_name',
              'reason', 'index1', 'comments1', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'time_created_at', 'created_by', 'point1', 'point2')

    for type in type_journal.iterator():
        data.append({"name": type.type_journal.name})

        for out in outfits.filter(type_journal=type.type_journal).iterator():
            data.append({"name": out.responsible_outfit.outfit})

            for event in all_event_names.filter(responsible_outfit=out.responsible_outfit,
                                                type_journal=type.type_journal).iterator():
                data.append({
                             "name": get_event_name(event)})

                for call in all_events.filter(object=event.object, ips=event.ips, circuit=event.circuit,
                                              name=event.name, responsible_outfit=out.responsible_outfit,
                                              type_journal=type.type_journal).order_by('date_from').iterator():
                    data.append({
                                 "name": "",
                                 "date_from": call.date_from,
                                 "date_to": get_date_to_ak(call, date),
                                 "region": call.point1.name + " - " + call.point2.name if call.point1 is not None else "",
                                 "index1": call.index1.index,
                                 "reason": call.reason.name,
                                 "comments1": call.comments1 if call.comments1 is not None else ""})

    template_name = 'pdf.html'
    template = get_template(template_name)
    html = template.render({"data": data, "all_tj":all_tj, "all_out":all_out,
                            "objs":objs, "ips":ips, "circ":cirs, "all_evs":all_evs, "date":date, "index":index})

    if 'DYNO' in os.environ:
        print('loading wkhtmltopdf path on heroku')
        WKHTMLTOPDF_CMD = subprocess.Popen(
            ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')],
            stdout=subprocess.PIPE).communicate()[0].strip()
    else:
        print('loading wkhtmltopdf path on localhost')
        WKHTMLTOPDF_CMD = ('/usr/local/bin/wkhtmltopdf/bin/wkhtmltopdf')

    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    options = {
        'margin-bottom': '20mm',
        'footer-center': '[page]',
        'header-left': 'Отчет ОПУ за ' + date,
        'header-spacing':2,
        'header-font-size':'12',
        'header-font-name':'Times New Roman'

    }
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="otchet-{}.pdf"'.format(date)
    response['Content-Disposition'] = f'attachment; filename="otchet-{date}.pdf"'
    return response




class OutfitWorkerGet(APIView):
    """статистика событий по предприятиям за сегодня"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        outfit = Outfit.objects.get(pk=pk)
        outfit_worker = OutfitWorker.objects.filter(outfit=outfit)
        serializer = OutfitWorkerListSerializer(outfit_worker, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutfitWorkerAPIView(ListAPIView):
    """возможность создавать сотрудников предприятий диспетчерам"""
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('outfit', 'name')


class OutfitWorkerCreateView(generics.CreateAPIView):
    """создание сотрудника - Ainur"""
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)


class OutfitWorkerEditView(generics.RetrieveUpdateAPIView):
    """редактирование сотрудника - Ainur"""
    lookup_field = 'pk'
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)


class OutfitWorkerDeleteAPIView(DestroyAPIView):
    """Удаления"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)
    queryset = OutfitWorker.objects.all().order_by('id')
    lookup_field = 'pk'


class CommentModelViewSet(viewsets.ModelViewSet):
    """Создание, удаление и список комментариеиив"""
    authentication_classes = (TokenAuthentication,)
    queryset = Comments.objects.all().order_by('id')
    serializer_class = CommentsSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser]

        return [permission() for permission in permission_classes]


class TypeJournalModelViewSet(viewsets.ModelViewSet):
    """Создание, удаление и список видо журналов"""
    authentication_classes = (TokenAuthentication,)
    queryset = TypeOfJournal.objects.all().order_by('id')
    serializer_class = TypeJournalSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser]

        return [permission() for permission in permission_classes]


class ReasonModelViewSet(viewsets.ModelViewSet):
    """Создание, удаление и список Reason"""
    authentication_classes = (TokenAuthentication,)
    queryset = Reason.objects.all().order_by('id')
    serializer_class = ReasonSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser]

        return [permission() for permission in permission_classes]


class IndexModelViewSet(viewsets.ModelViewSet):
    """Создание, удаление и список Reason"""
    authentication_classes = (TokenAuthentication,)
    queryset = Index.objects.all().order_by('id')
    serializer_class = IndexSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser]
        return [permission() for permission in permission_classes]


#Создание произвольного события. Будут показываться список произвольных событий, где поле name !=None. Ainur
class EventUnknownCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)
    """Создания Unknown Event"""

    def post(self, request):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save( created_by=self.request.user.profile)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, name=event.name,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DamageReportListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = DamageReportListSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get("date_from", "")
        date_to = self.request.query_params.get("date_to", "")
        outfit = self.request.query_params.get("outfit", "")
        if date_from == "" or date_to == "":
            return []
        queryset = Event.objects.\
            defer("reason", "type_journal", "created_by", "contact_name", "send_from", "customer", "index1",
                  "circuit", "ips", "name").\
            filter(Q(object__tpo1__index="35") | Q(object__tpo1__index="51") | Q(object__tpo2__index="35") |
                   Q(object__tpo2__index="51"), object__name__regex=r"^(?:K|К).[^-]+(?:-.[^-]+){0,1}\Z",
                   index1__index="1", callsorevent=False, date_to__date__gte=date_from, date_to__date__lte=date_to).\
            prefetch_related("object", "responsible_outfit", "point1", "point2")
        if outfit != "":
            queryset = queryset.filter(responsible_outfit=outfit)
        return queryset


class DamageUpdateAPIView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser)
    queryset = Event.objects.filter(callsorevent=False)
    serializer_class = DamageUpdateSerializer
    lookup_field = "pk"


class InternationalDamageReportListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InternationalDamageReportListSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get("date_from", "")
        date_to = self.request.query_params.get("date_to", "")

        if date_from == "" or date_to == "":
            return []
        queryset = Event.objects. \
            defer("reason", "type_journal", "created_by", "contact_name", "send_from", "customer", "index1", "name"). \
            exclude(Q(object__tpo1__index="35") | Q(object__tpo1__index="51") | Q(object__tpo2__index="35") |
                    Q(object__tpo2__index="51") | Q(ips__tpo__index="35") | Q(ips__tpo__index="51") |
                    Q(circuit__point1__tpo__index="35") | Q(circuit__point2__tpo__index="35") |
                    Q(circuit__point1__tpo__index="51") | Q(circuit__point2__tpo__index="51")). \
            filter(index1__index="1", callsorevent=False, date_to__date__gte=date_from, date_to__date__lte=date_to,
                   name__isnull=True).\
            prefetch_related("object", "circuit", "ips", "responsible_outfit", "point1", "point2")

        return queryset


class TechStopReportListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = TechStopReportListSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        customer = self.request.query_params.get("customer")
        queryset = Event.objects.filter(index1__index="1", callsorevent=False).filter(Q(object__form_customer__isnull=False)|Q(circuit__form_customer__isnull=False)).prefetch_related("object", "circuit", "ips", "responsible_outfit", "point1", "point2")
        queryset = event_form_customer_filter_date_from_date_to_and_customer(queryset, date_from, date_to, customer)
        return queryset



