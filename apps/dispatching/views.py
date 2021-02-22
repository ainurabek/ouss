import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import EventListSerializer, CommentsSerializer, TypeJournalSerializer,\
    ReasonSerializer, IndexSerializer, CallsCreateSerializer, ReportSerializer
from .services import get_minus_date, ListFilterAPIView, get_event_name
from ..accounts.permissions import SuperUser, IsDispOnly, IngenerUser
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
    #фильтр по хвостам + за сегодня

        today = datetime.date.today()
        queryset1 = self.queryset.exclude(index1__index='4')
        queryset2 = self.queryset.filter(created_at=today)
        queryset = queryset1.union(queryset2).order_by('id')
    # фильтр  по дате создания, без времени + хвосты за предыдущие дни

        created_at = self.request.query_params.get('created_at', None)
        type_journal = self.request.query_params.get('type_journal', None)
        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        index1 = self.request.query_params.get('index1', None)
        name = self.request.query_params.get('name', None)

        if created_at is not None and created_at != '':
            q1 = self.queryset.filter(created_at__lte=created_at).exclude(index1__index='4')
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
        calls = Event.objects.get(pk=pk).event_id_parent.all().order_by("-date_from")
        serializer = self.get_serializer(calls, many=True)
        return Response(serializer.data)


class EventIPCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
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

            response = {"data": "Событие создано успешно"}
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCircuitCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
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
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
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

            response = {"data": "Событие создано успешно"}

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCallsCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
    """Создания Event"""

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = CallsCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(id_parent=event, created_by=self.request.user.profile,
                                       callsorevent=False)

            all_calls = event.event_id_parent.all()
            prev = all_calls.filter(date_from__lt = instance.date_from).order_by('-date_from')[0] if all_calls.filter(date_from__lt = instance.date_from).count() != 0  else None

            next = all_calls.filter(date_from__gt=instance.date_from).order_by('date_from')[0] if all_calls.filter(date_from__gt=instance.date_from).count() != 0 else None

            if prev is not None and next is not None:

                prev.date_to = instance.date_from
                prev.save()
                next.previous = None
                next.save()
                instance.date_to = next.date_from
                instance.previous = prev
                instance.save()
                next.previous = instance
                next.save()
            elif prev is None and next is not None:

                instance.date_to = next.date_from
                instance.save()
                next.previous = instance
                next.save()
                event.date_from = instance.date_from
                event.save()
            elif prev is not None and next is None:
                event.date_to = instance.date_from
                event.index1 = instance.index1
                instance.previous = prev
                prev.date_to = instance.date_from
                event.save()
                instance.save()
                prev.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdateAPIView(UpdateAPIView):
    """Редактирования event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser|IsDispOnly, IngenerUser)
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    def perform_update(self, serializer):
        #это меняет дату конца предыдущего события
        date_from = str(self.get_object().date_from)
        instance = serializer.save()


        if instance.id_parent is not None:
            all_calls = instance.id_parent.event_id_parent.all().order_by('-date_from')
            next = all_calls.filter(date_from__gt=instance.date_from)

            if date_from != instance.date_from and instance.previous is not None:
                instance.previous.date_to = instance.date_from
                instance.previous.save()

            if next.count() == 0:
                instance.id_parent.date_to = instance.date_from
                instance.id_parent.index1 = instance.index1
                instance.id_parent.save()

            serializer.save()


class EventDeleteAPIView(DestroyAPIView):
    """Удаление события  по звонкам"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsDispOnly, IngenerUser)
    queryset = Event.objects.all()
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if instance.id_parent is None:
            instance.delete()
            return

        main_event = get_object_or_404(Event, pk=instance.id_parent.pk)
        previous_event = instance.previous

        if Event.objects.filter(previous=instance).exists():
            next_event = instance.event_previous
        else:
            next_event = None


        if previous_event is not None and next_event is not None:
            instance.delete()
            previous_event.date_to = next_event.date_from
            next_event.previous = previous_event
            next_event.save()
            previous_event.save()

        elif previous_event is None and next_event is None:
            instance.delete()
            main_event.delete()

        elif next_event is None:
            instance.delete()
            main_event.date_to = previous_event.date_from
            main_event.index1 = previous_event.index1
            main_event.save()
            previous_event.date_to = None
            previous_event.save()

        else:
            main_event.date_from = next_event.date_from
            main_event.index1 = next_event.index1
            main_event.save()
            instance.delete()



@permission_classes([IsAuthenticated,])
def get_dates_and_counts_week(request):
    """статистика событий за неделю"""
    data = {}
    dates = Event.objects.filter(created_at__gte=get_minus_date(days=7)).\
        exclude(previous__isnull=True, callsorevent=False).order_by('created_at').distinct('created_at')

    teams_data = [
        {"day": date.created_at.strftime("%A"), "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).
            exclude(previous__isnull=True, callsorevent=False).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated,])
def get_dates_and_counts_month(request):
    """статистика событий за месяц"""
    data = {}
    dates = Event.objects.filter(created_at__gte=get_minus_date(days=30)).\
        exclude(previous__isnull=True, callsorevent=False).order_by('created_at').distinct('created_at')
    teams_data = [
        {"day": date.created_at.day, "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).
            exclude(previous__isnull=True, callsorevent=False).count() }
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
        exclude(previous__isnull=True, callsorevent=False).order_by('date_from').distinct('date_from')
    teams_data = [
        {"time": date.date_from, "counts": Event.objects.filter(date_from=date.date_from).
            exclude(previous__isnull=True, callsorevent=False).count()}
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated, ])
def get_outfit_statistics_for_a_month(request):
    """статистика событий по предприятиям за месяц"""
    month = get_minus_date(days=30)
    dates = Event.objects.filter(created_at__gte=month).\
        exclude(previous__isnull=True, callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=month).
             exclude(previous__isnull=True, callsorevent=False).count()}
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)

@permission_classes([IsAuthenticated,])
def get_outfit_statistics_for_a_week(request):
    """статистика событий по предприятиям за неделю"""
    week = get_minus_date(days=7)
    dates = Event.objects.filter(created_at__gte=week).exclude(previous__isnull=True, callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=week).
             exclude(previous__isnull=True, callsorevent=False).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)

@permission_classes([IsAuthenticated,])
def get_outfit_statistics_for_a_day(request):
    """статистика событий по предприятиям за сегодня"""
    day = datetime.date.today()
    dates = Event.objects.filter(created_at__gte=day).\
        exclude(previous__isnull=True, callsorevent=False).order_by('responsible_outfit').distinct('responsible_outfit')
    teams_data = [
        {"outfit": date.responsible_outfit.outfit,
         "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=day).
             exclude(previous__isnull=True, callsorevent=False).count() }
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
    queryset = Event.objects.filter(date_to=None).exclude(previous__isnull=True,
                                                          callsorevent=False).exclude(index1__index='4')

@permission_classes([IsAuthenticated, SuperUser|IsDispOnly])
def get_report_object(request):
    date = request.GET.get("date")
    index = request.GET.get("index")
    if date is None or date == "":
        date = datetime.date.today()

    all_event_completed = Event.objects.filter(callsorevent=True, created_at=date, index1__index='4')
    all_event_uncompleted = Event.objects.filter(created_at__lte=date, callsorevent=True).exclude(index1__index='4')
    all_event = all_event_completed | all_event_uncompleted
    all_calls = Event.objects.filter(callsorevent=False)
    if index is not None and index != "":
        all_calls = all_calls.filter(index1_id=index)
    type_journal = (all_event_completed | all_event_uncompleted).order_by("type_journal").distinct("type_journal")
    outfits = (all_event_completed | all_event_uncompleted).order_by("responsible_outfit").distinct("responsible_outfit")
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
            for event in all_event.filter(responsible_outfit=out.responsible_outfit, type_journal=type.type_journal):
                data.append({"outfit": None,
                             "name": get_event_name(event),
                             "type_journal": None,
                             "date_from": None,
                             "date_to": None,
                             "region": None,
                             "index1": None,
                             "reason": None,
                             "comments1": None})
                calls_count = 0
                for call in all_calls.filter(id_parent=event).exclude(index1__index='4'):
                    data.append({"outfit": None,
                                 "name": get_event_name(call),
                                 "type_journal": None,
                                 "date_from": call.date_from,
                                 "date_to": call.date_to,
                                 "region": call.point1.name + " - " + call.point2.name if call.point1 is not None else "",
                                 "index1": call.index1.index,
                                 "reason": call.reason.name,
                                 "comments1": call.comments1})
                    calls_count += 1
                if calls_count == 0:
                    data.pop()

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

