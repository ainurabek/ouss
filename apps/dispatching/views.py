import datetime
from datetime import date
from itertools import groupby

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import EventListSerializer, CircuitEventList, ObjectEventSerializer, \
    IPSSerializer, CommentsSerializer, EventUnknownSerializer, TypeJournalSerializer,\
    ReasonSerializer, IndexSerializer, CallsCreateSerializer, ReportSerializer
from .services import get_minus_date, ListFilterAPIView, get_event_name
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object, IP, OutfitWorker, Outfit
from .serializers import EventCreateSerializer, EventDetailSerializer
from rest_framework import viewsets, generics

from ..opu.objects.serializers import OutfitWorkerListSerializer, OutfitWorkerCreateSerializer

now = date.today()
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView

from .models import Event, TypeOfJournal, Comments, Reason, Index
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication


########API
#listevent
class EventListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=True)
    lookup_field = 'pk'
    serializer_class = EventListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == "retrieve":
            return EventDetailSerializer

    # событие считается завершенным, если придать ему второй индекс, пока его нет, оно будет висеть как незавершенное

    def get_queryset(self):
    #фильтр по хвостам + за сегодня

        today = datetime.date.today()
        queryset1 = self.queryset.exclude(index1__id=11)
        queryset2 = self.queryset.filter(created_at=today)
        queryset = queryset1.union(queryset2).order_by('-created_at')
    # фильтр  по дате создания, без времени + хвосты за предыдущие дни

        created_at = self.request.query_params.get('created_at', None)
        type_journal = self.request.query_params.get('type_journal', None)
        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        index1 = self.request.query_params.get('index1', None)
        name = self.request.query_params.get('name', None)

        if created_at is not None and created_at != '':
            q1 = self.queryset.filter(created_at__lte=created_at).exclude(index1=11)
            q2 = self.queryset.filter(created_at=created_at)
            queryset = q1.union(q2)

        if type_journal is not None and type_journal != '':
            queryset = self.queryset.filter(type_journal=type_journal)
        if responsible_outfit is not None and responsible_outfit != '':
            queryset = self.queryset.filter(responsible_outfit=responsible_outfit)
        if index1 is not None and index1 != '':
            queryset = self.queryset.filter(index1=index1)
        if name is not None and name != '':
            queryset = self.queryset.filter(name=name)

        return queryset


    def retrieve(self, request, pk=None):
        calls = Event.objects.filter(id_parent_id=pk).order_by("-created_at")
        serializer = self.get_serializer(calls, many=True)
        return Response(serializer.data)


class IPEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = IP.objects.all()
    serializer_class = IPSSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('point_id', 'object_id')


class EventIPCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""
    def post(self, request, pk):
        ip = IP.objects.get(pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(ips=ip, created_by=self.request.user.profile, created_at=now)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, ips=event.ips,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )
            # update_period_of_time(instance=obj)
            response = {"data": "Событие создано успешно"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CircuitEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Circuit.objects.all()
    serializer_class = CircuitEventList
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('id_object', 'customer', 'name', 'type_using')

#cirxuit create - Ainur
class EventCircuitCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""

    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(circuit=circuit, created_by=self.request.user.profile, created_at=now)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, circuit=event.circuit,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )
            # update_period_of_time(instance=obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#obj - Ainur
class ObjectEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectEventSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('name', 'point1', 'point2', 'id_outfit', 'customer')

#obj create - Ainur
class EventObjectCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""

    def post(self, request, pk):
        object = get_object_or_404(Object, pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(object=object, created_by=self.request.user.profile, created_at=now)
            Event.objects.create(id_parent=event, callsorevent=False, created_at=event.created_at,
                                 date_from=event.date_from, index1=event.index1,
                                 type_journal=event.type_journal, point1=event.point1, point2=event.point2,
                                 reason=event.reason, comments1=event.comments1, object=event.object,
                                 responsible_outfit=event.responsible_outfit, send_from=event.send_from,
                                 customer=event.customer, created_by=event.created_by, contact_name=event.contact_name,
                                 )

            response = {"data": "Событие создано успешно"}

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCallsCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""

    def post(self, request, pk, id):
        event = get_object_or_404(Event, pk=pk)
        previous_event = get_object_or_404(Event, pk=id)
        serializer = CallsCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(id_parent=event, created_by=self.request.user.profile, created_at=now,
                                       callsorevent=False, previous=previous_event)
            response = {"data": "Звонок создано успешно"}
            event.date_to = instance.date_from
            event.index1 = instance.index1
            event.save()
            previous_event.date_to = instance.date_from
            previous_event.save()

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#чтобы передавать фронту нужно
class OutfitWorkerGet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        outfit = Outfit.objects.get(pk=pk)
        outfit_worker = OutfitWorker.objects.filter(outfit=outfit)
        serializer = OutfitWorkerListSerializer(outfit_worker, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# event update - Ainur
class EventUpdateAPIView(UpdateAPIView):
    """Редактирования event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer


#удаление события - Ainur
class EventDeleteAPIView(DestroyAPIView):
    """Удаления event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        main_event = get_object_or_404(Event, pk=instance.id_parent.pk)
        if instance.previous is not None:
            previous_event = get_object_or_404(Event, pk=instance.previous.pk)
            main_event.date_to = previous_event.date_to
            main_event.index1 = previous_event.index1
            main_event.save()
            previous_event.date_to = None
            previous_event.save()
        instance.delete()
        if main_event.event_id_parent.count() == 0:
            main_event.delete()





#Создание произвольного события. Будут показываться список произвольных событий, где поле name !=None. Ainur
class UnknownEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.exclude(name__isnull=True)
    serializer_class = EventUnknownSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('name',)


class EventUnknownCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Unknown Event"""

    def post(self, request):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save( created_by=self.request.user.profile, created_at=now)
            response = {"data": "Событие создано успешно"}
            # update_period_of_time(instance=obj)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardTodayEventList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        queryset = Event.objects.filter(created_at=today)
        serializer = EventListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_dates_and_counts_week(request):
    data = {}
    dates = Event.objects.filter(created_at__gte=get_minus_date(days=7)).distinct('created_at')
    teams_data = [
        {"day": date.created_at.strftime("%A"), "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)


def get_dates_and_counts_month(request):
    data = {}
    dates = Event.objects.filter(created_at__gte=get_minus_date(days=30)).distinct('created_at')
    teams_data = [
        {"day": date.created_at.day, "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)


def get_dates_and_counts_today(request):
    data = {}
    time = datetime.date.today()
    dates = Event.objects.filter(date_from__gte=time).distinct('date_from__hour')
    teams_data = [
        {"time": date.date_from.time(), "counts": Event.objects.filter(date_from=date.date_from).count()}
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)


def get_outfit_statistics_for_a_month(request):
    month = get_minus_date(days=30)
    dates = Event.objects.filter(created_at__gte=month).distinct('responsible_outfit')
    all_data = Event.objects.filter(created_at__gte=month).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=month).count()/all_data)*100,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=month).count()}
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


def get_outfit_statistics_for_a_week(request):
    week = get_minus_date(days=7)
    dates = Event.objects.filter(created_at__gte=week).distinct('responsible_outfit')
    all = Event.objects.filter(created_at__gte=week).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit, "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=week).count()/all)*100, "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=week).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


def get_outfit_statistics_for_a_day(request):
    day = datetime.date.today()
    dates = Event.objects.filter(created_at__gte=day).distinct('responsible_outfit')
    all = Event.objects.filter(created_at__gte=day).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit, "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=day).count()/all)*100, "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=day).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


class CompletedEvents(ListFilterAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer
    queryset = Event.objects.filter(callsorevent=False, index1=11)


class UncompletedEventList(ListFilterAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer
    # queryset = Event.objects.exclude(index2__isnull=True)
    queryset = Event.objects.all()


#Отчет дисп службы
class ReportEventDisp(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportSerializer

#в отчете выходят данные за тот заданный период +хвосты(незакрытые)
    def get_queryset(self):
        queryset = Event.objects.all()
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if date_to == '' and date_from != '':
            queryset1 = queryset.exclude(index1__id=11, created_at__gte=date_from)
            queryset2 = queryset.filter(created_at=date_from)
            queryset = queryset1.union(queryset2)
        elif date_to != '' and date_from == '':
            queryset1 = queryset.exclude(index1__id=11, created_at__gte=date_to)
            queryset2 = queryset.filter(created_at=date_to)
            queryset = queryset1.union(queryset2)
        elif date_to != '' and date_from != '':
            queryset1 = queryset.exclude(index1__id=11, created_at__gte=date_to, created_at__lte=date_from)
            # queryset1 = queryset.filter(index2=None, created_at__lte=date_to, created_at__gte=date_from)
            queryset2 = queryset.filter(created_at__gte=date_from, created_at__lte=date_to)
            queryset = queryset1.union(queryset2)

        return queryset
      
      
def get_report_object(request):
    today = datetime.date.today()
    # dates = Event.objects.filter(created_at=today)
    teams_data = []
    # for i in dates:
    #     if i.object !=None:
    #         objects = [
    #             {'name':i.object.name, "date_from": i.date_from,
    #              "date_to":i.date_to, 'index1':i.index1.name, "id":i.id}
    #         ]
    #         teams_data.append(objects)
    #     if i.circuit !=None:
    #         circuits = [
    #             {'name': i.circuit.name, "date_from": i.date_from,
    #              "date_to": i.date_to, 'index1': i.index1.name, "id": i.id}
    #
    #         ]
    #         teams_data.append(circuits)
    #     if i.ips !=None:
    #         ips = [
    #             {'name': i.ips.point_id.point, "date_from": i.date_from,
    #              "date_to": i.date_to, 'index1': i.index1.name, "id": i.id}
    #
    #         ]
    #         teams_data.append(ips)
    #     if i.name !=None:
    #         unknown = [
    #             {'name': i.name, "date_from": i.date_from,
    #              "date_to": i.date_to, 'index1': i.index1.name, "id": i.id}
    #
    #         ]
    #         teams_data.append(unknown)

    # next(item for item in teams_data if item["name"] == "Pam")
    # all_calls = Event.objects.filter(callsorevent=False)

    all_event = Event.objects.filter(callsorevent=True)
    all_calls = Event.objects.filter(callsorevent=False)
    type_journal = Event.objects.order_by("type_journal").distinct("type_journal")
    outfits = Event.objects.order_by("responsible_outfit").distinct("responsible_outfit")

    data = [
        {"type_journal": type.type_journal.name,
         "outfits":
             [{"outfit": outfit.responsible_outfit.outfit,
                      "events": [
                          {"event": get_event_name(event),
                                  "calls": [{
                        "id": call.id,
                        "name": get_event_name(call),
                        "date_from": call.date_from,
                        "date_to": call.date_to,
                        "region": call.point1.point + " - " + call.point2.point,
                        "index1": call.index1.name,
                        "comments1": call.comments1
                    }
                                      for call in all_calls.filter(id_parent=event, responsible_outfit=outfit.responsible_outfit, type_journal=type.type_journal).exclude(index1_id=11)]}
                                 for event in all_event.filter(responsible_outfit=outfit.responsible_outfit)]}
                     for outfit in outfits.filter(type_journal=type.type_journal)]} for type in type_journal]
    # for type in type_journal:
    #     res = {}
    #     res["type_journal"] = type.type_journal.name
    #     res["outfits"] = []
    #     for outfit in outfits.filter(type_journal=type.type_journal):
    #         out = {}
    #         out["outfit"] = outfit.responsible_outfit.outfit
    #         out["events"] = []
    #         for event in all_event.filter(responsible_outfit=outfit.responsible_outfit):
    #             event_name = get_event_name(event)
    #             e = {"event": event_name}
    #             e["calls"] = []
    #             for call in all_calls.filter(id_parent=event, responsible_outfit=outfit.responsible_outfit, type_journal=type.type_journal).exclude(index1_id=11):
    #                 call_name = get_event_name(call)
    #                 e["calls"].append({
    #                     "id": call.id,
    #                     "name": call_name,
    #                     "date_from": call.date_from,
    #                     "date_to": call.date_to,
    #                     "region": call.point1.point + " - " + call.point2.point,
    #                     "index1": call.index1.name,
    #                     "comments1": call.comments1
    #                 })
    #             out["events"].append(e)
    #         res["outfits"].append(out)
    #     data.append(res)

    return JsonResponse(data, safe=False)

#возможность создавать сотрудников предприятий диспетчерам
class OutfitWorkerAPIView(ListAPIView):
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('outfit', 'name')


#создание сотрудника - Ainur
class OutfitWorkerCreateView(generics.CreateAPIView):
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


#редактирование сотрудника - Ainur
class OutfitWorkerEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


#сотрудника удаление - Ainur
class OutfitWorkerDeleteAPIView(DestroyAPIView):
    """Удаления"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OutfitWorker.objects.all()
    lookup_field = 'pk'



#Создание, удаление и список комментариеиив
class CommentModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'pk'

#Создание, удаление и список видо журналов
class TypeJournalModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TypeOfJournal.objects.all()
    serializer_class = TypeJournalSerializer
    lookup_field = 'pk'

#Создание, удаление и список Reason
class ReasonModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    lookup_field = 'pk'

#Создание, удаление и список Reason
class IndexModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    lookup_field = 'pk'