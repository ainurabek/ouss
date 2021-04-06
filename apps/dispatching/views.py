import datetime
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import EventListSerializer, CommentsSerializer, TypeJournalSerializer, \
    ReasonSerializer, IndexSerializer, CallsCreateSerializer
from .services import get_minus_date, ListFilterAPIView, get_event_name, get_date_to
from ..accounts.permissions import SuperUser, IsDispOnly, IngenerUser, DateCheck
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object, IP, OutfitWorker, Outfit, Point
from .serializers import EventCreateSerializer, EventDetailSerializer
from rest_framework import viewsets, generics

from ..opu.objects.serializers import OutfitWorkerListSerializer, OutfitWorkerCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView

from .models import TypeOfJournal, Comments, Reason, Index, Event
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework.decorators import permission_classes



class EventListAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly)
    queryset = Event.objects.filter(callsorevent=True).prefetch_related('object', 'circuit', 'ips', 'index1',
                                                                        'responsible_outfit')

    lookup_field = 'pk'
    serializer_class = EventListSerializer


    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == "retrieve":
            return EventDetailSerializer
    # событие считается завершенным, если придать ему второй индекс, пока его нет, оно будет висеть как незавершенное

    def get_queryset(self):
        created_at = self.request.query_params.get('created_at', None)

        type_journal = self.request.query_params.get('type_journal', None)
        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        index1 = self.request.query_params.get('index1', None)
        name = self.request.query_params.get('name', None)
    #фильтр по хвостам + за сегодня

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
        queryset = queryset.filter(Q(date_to__date=created_at) | Q(date_to__date=None)|Q(date_from__date=created_at)) | (queryset.exclude(index1__index='4', date_to__date__lt=created_at).filter(date_from__date__lt=created_at))
        return queryset

    def retrieve(self, request, pk=None):
        calls = Event.objects.get(pk=pk).event_id_parent.all().order_by("-date_from")

        serializer = self.get_serializer(calls, many=True)

        return Response(serializer.data)


class EventDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly)


    def get(self, request, pk=None):
        created_at = request.GET.get("created_at")

        calls = Event.objects.get(pk=pk).event_id_parent.filter(date_from__date__lte=created_at).order_by("-date_from")

        serializer = EventDetailSerializer(calls, many=True)
        return Response(serializer.data)


class EventIPCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,   SuperUser|IsDispOnly, SuperUser|IngenerUser)
    """Создания Event"""
    def post(self, request, pk):

        point = Point.objects.get(pk=pk)
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
                                  contact_name=event.contact_name,
                                 )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCircuitCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,   SuperUser|IsDispOnly, SuperUser|IngenerUser )
    """Создания Event"""

    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
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
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, SuperUser|IngenerUser)
    """Создания Event"""

    def post(self, request, pk):
        object = get_object_or_404(Object, pk=pk)
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
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, SuperUser|IngenerUser,)
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
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser|SuperUser, DateCheck)
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    def perform_update(self, serializer):

        instance = serializer.save()
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
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, SuperUser|IngenerUser, DateCheck)
    queryset = Event.objects.all()
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if instance.id_parent is None:
            instance.delete()
            return
        all_calls = instance.id_parent.event_id_parent.all().order_by('-date_from')
        instance.delete()
        i = 0

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


@permission_classes([IsAuthenticated, SuperUser|IsDispOnly])
def get_report_object(request):
    date = request.GET.get("date")

    index = request.GET.get("index")

    all_events = Event.objects.filter(Q(date_to__date__gte=date) |Q(date_to__date = None), callsorevent=False).exclude(index1__index='4')
    all_events =all_events.filter(date_from__date__lte=date)

    all_event_names = all_events.order_by('ips_id', 'object_id', 'circuit_id', 'name').distinct('ips_id', 'object_id', 'circuit_id', 'name')

    if index is not None and index != "":
        all_events = all_events.filter(index1_id=index)


    type_journal = all_event_names.order_by("type_journal").distinct("type_journal")
    outfits = all_event_names.order_by("responsible_outfit").distinct("responsible_outfit")
    data = []

    for type in type_journal:
        data.append({"type_journal": type.type_journal.name,
                     "outfit": None,
                     "name": None,
                     "date_from": None,
                     "date_to": None,
                     "region": None,
                     "index1": None,
                     "reason": None,
                     "comments1": None})

        for out in outfits.filter(type_journal=type.type_journal):
            data.append({"outfit": out.responsible_outfit.outfit,
                     "name": None,
                     "type_journal": None,
                     "date_from": None,
                     "date_to": None,
                     "region": None,
                     "index1": None,
                     "reason": None,
                     "comments1": None})

            for event in all_event_names.filter(responsible_outfit=out.responsible_outfit):
                data.append({"outfit": None,
                             "name": get_event_name(event),
                             "type_journal": None,
                             "date_from": None,
                             "date_to": None,
                             "region": None,
                             "index1": None,
                             "reason": None,
                             "comments1": None})

                for call in all_events.filter(object=event.object, ips=event.ips, circuit=event.circuit, name= event.name).order_by('date_from'):
                    data.append({"outfit": None,
                                 "name": '-',
                                 "type_journal": None,
                                 "date_from": call.date_from,
                                 "date_to": get_date_to(call, date),
                                 "region": call.point1.name + " - " + call.point2.name if call.point1 is not None else "",
                                 "index1": call.index1.index,
                                 "reason": call.reason.name,
                                 "comments1": call.comments1})



    return JsonResponse(data, safe=False)


class OutfitWorkerGet(APIView):
    """статистика событий по предприятиям за сегодня"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)


class OutfitWorkerEditView(generics.RetrieveUpdateAPIView):
    """редактирование сотрудника - Ainur"""
    lookup_field = 'pk'
    queryset = OutfitWorker.objects.all()
    serializer_class = OutfitWorkerCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)


class OutfitWorkerDeleteAPIView(DestroyAPIView):
    """Удаления"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
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
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser]

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
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser]

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
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser]

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
            permission_classes = [IsAuthenticated, SuperUser|IsDispOnly, IngenerUser]

        return [permission() for permission in permission_classes]

#Создание произвольного события. Будут показываться список произвольных событий, где поле name !=None. Ainur
class EventUnknownCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
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

            # update_period_of_time(instance=obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)