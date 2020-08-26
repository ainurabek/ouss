import datetime
from datetime import date, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse

from .serializers import EventListSerializer, CircuitEventList, ObjectEventSerializer, \
    IPSSerializer, CommentsSerializer, EventUnknownSerializer
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object, IP, OutfitWorker, Outfit
from .serializers import EventCreateSerializer, EventDetailSerializer
from rest_framework import viewsets, generics

from ..opu.objects.serializers import OutfitWorkerListSerializer, OutfitWorkerCreateSerializer

now = date.today()
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from django.views.generic import ListView
from .forms import EventForm
from .models import Event, TypeOfJournal, Comments
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication

class JournalList(ListView):
    """Список заявок"""
    model = TypeOfJournal
    template_name = 'dispatching/types_journals.html'
    context_object_name = 'types_journals'

    def get_context_data(self, *, pk=None, **kwargs):
        types_journal = TypeOfJournal.objects.all()
        context = {'types_journal': types_journal}
        return super().get_context_data(**context)


# def event_list(request, journal_pk):
#     journal = get_object_or_404(TypeOfJournal, pk=journal_pk)
#     events = Event.objects.filter(type_journal=journal)
#     choices = Choice.objects.all()
#     return render(request, 'dispatching/event_list.html', {
#         'events': events, 'choices': choices, 'journal': journal
#     })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'dispatching/event_detail.html', {
        'event': event
    })
# class EventCreateView(View):
#     """Создания отключения"""
#     def post(self, request, pk):
#
#         choice = Choice.objects.get(pk=pk)
#         print(choice)
#         form = EventForm(request.POST or None)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.created_by = self.request.user.profile
#             print(form.created_by)
#             form.choice = choice
#             form.save()
#             return redirect('apps:dispatching:event_list')
#
#     def get(self, request, pk):
#         choice = Choice.objects.get(pk=pk)
#         form = EventForm()
#         return render(request, 'dispatching/request_create.html', {'form': form,
#                                                                    'choice': choice
#                                                                    })

def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            request1 = form.save(commit=False)
            request1.created_by = request.user.profile
            request1.created_at = datetime.datetime.now()
            request1.save()
            return redirect('apps:dispatching:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dispatching/request_create.html', {'form': form})


def event_delete(request, pk):
    Event.objects.get(pk=pk).delete()
    return redirect('apps:dispatching:event_list')

########API
#listevent
class EventListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    queryset = Event.objects.all()
    lookup_field = 'pk'
    serializer_class = EventListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('type_journal', 'contact_name',
                        'reason', 'index1', 'index2', 'responsible_outfit', 'send_from', 'created_at', 'name')


    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == "retrieve":
            return EventDetailSerializer

    def get_queryset(self):
        #событие считается завершенным, если придать ему второй индекс, пока его нет, оно будет висеть как незавершенное

        today = datetime.date.today()
        queryset1 = Event.objects.filter(index2=None).distinct('object', 'circuit', 'ips')
        queryset2 = Event.objects.filter(created_at=today).distinct('object', 'circuit', 'ips')
        queryset=queryset1.union(queryset2).order_by('-created_at')
        #фильтр по хвостам  за сегодня



        date_from_from = self.request.query_params.get('date_from_from', None)
        date_to_from = self.request.query_params.get('date_to_from', None)
        created_at = self.request.query_params.get('created_at', None)

# фильтр  по дате создания, без времени
        if created_at is not None and created_at != "":
            queryset = queryset.filter(created_at=created_at)

#фильтр для поля Начало
        if date_from_from is not None and date_from_from != "":
            date_from_from+='T00:00:00'
            queryset = queryset.filter(date_from__gte=date_from_from)
        if date_to_from is not None and date_to_from != "":
            date_to_from += 'T23:59:00'
            queryset = queryset.filter(date_from__lte=date_to_from)
# фильтр для поля Конец
        date_from_to = self.request.query_params.get('date_from_to', None)
        date_to_to = self.request.query_params.get('date_to_to', None)

        if date_from_to is not None and date_from_to != "":
            date_from_to += 'T00:00:00'
            queryset = queryset.filter(date_to__gte=date_from_to)
        if date_to_to is not None and date_to_to != "":
            date_to_to += 'T23:59:00'
            queryset = queryset.filter(date_to__lte=date_to_to)

        return queryset


    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Event, pk=pk)
        if instance.object is not None:
            instance = Event.objects.filter(object=instance.object)
        elif instance.circuit is not None:
            instance = Event.objects.filter(circuit=instance.circuit)
        elif instance.ips is not None:
            instance = Event.objects.filter(ips=instance.ips)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

#ip-Ainur
class IPEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = IP.objects.all()
    serializer_class = IPSSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('point_id', 'object_id')

#create- Ainur
class EventIPCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""
    def post(self, request, pk):
        ip = IP.objects.get(pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ips=ip, created_by=self.request.user.profile, created_at=now)
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
            serializer.save(circuit=circuit, created_by=self.request.user.profile, created_at=now)
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
            serializer.save(object=object, created_by=self.request.user.profile, created_at=now)
            response = {"data": "Событие создано успешно"}
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
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# статистика событий за неделю - Айнур
def get_dates_and_counts_week(request):
    data = {}
    week = datetime.date.today() - timedelta(days=7)
    dates = Event.objects.filter(created_at__gte=week).distinct('created_at')
    teams_data = [
        {"day": date.created_at.weekday(), "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)

# статистика событий за месяц - Айнур
def get_dates_and_counts_month(request):
    data = {}
    month = datetime.date.today() - timedelta(days=30)
    dates = Event.objects.filter(created_at__gte=month).distinct('created_at')
    teams_data = [
        {"day": date.created_at.day, "date": date.created_at, "counts": Event.objects.filter(created_at=date.created_at).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)


# статистика событий за сегодня - Айнур
def get_dates_and_counts_today(request):
    data = {}
    time = timedelta - timedelta(hours=24)

    dates = Event.objects.filter(date_from__gte=time).distinct('date_from__hour')
    teams_data = [
        {"time": date.date_from.hour, "counts": Event.objects.filter(date_from=date.date_from).count() }
        for date in dates
    ]
    data["dates"] = teams_data
    return JsonResponse(data, safe=False)



def get_outfit_statistics_for_a_month(request):
    data = {}
    month = datetime.date.today() - timedelta(days=30)
    dates = Event.objects.filter(created_at__gte=month).distinct('responsible_outfit')
    all = Event.objects.filter(created_at__gte=month).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit, "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=month).count()/all)*100, "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=month).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


def get_outfit_statistics_for_a_week(request):
    data = {}
    week = datetime.date.today() - timedelta(days=7)
    dates = Event.objects.filter(created_at__gte=week).distinct('responsible_outfit')
    all = Event.objects.filter(created_at__gte=week).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit, "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=week).count()/all)*100, "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=week).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


def get_outfit_statistics_for_a_day(request):
    data = {}
    day = datetime.date.today()
    dates = Event.objects.filter(created_at__gte=day).distinct('responsible_outfit')
    all = Event.objects.filter(created_at__gte=day).count()
    teams_data = [
        {"outfit": date.responsible_outfit.outfit, "percent": (Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=day).count()/all)*100, "counts": Event.objects.filter(responsible_outfit=date.responsible_outfit, created_at__gte=day).count() }
        for date in dates
    ]

    return JsonResponse(teams_data, safe=False)


class CompletedEvents(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer

    def get_queryset(self):
        queryset = Event.objects.exclude(index2=None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)


        if date_to == "" and date_from == "":
            week = datetime.date.today() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week)

        else:

            if date_to == "":
                queryset = queryset.filter(created_at=date_from)

            else:
                if date_to != '':
                    queryset = queryset.filter(created_at__lte=date_to)
                if date_from != '':
                    queryset = queryset.filter(created_at__gte=date_from)

        return queryset


class UncompletedEventList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    def get_queryset(self):
        queryset = Event.objects.all()
        date_from = queryset.query_params.get('date_from', None)
        date_to = queryset.query_params.get('date_to', None)

        if date_from == '' and date_to == '':
            week = datetime.date.today() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week)
        else:
            if date_to == "":
                queryset = queryset.filter(created_at=date_from)
            else:
                if date_to != '':
                    queryset = queryset.filter(created_at__lte=date_to)
                if date_from != '':
                    queryset = queryset.filter(created_at__gte=date_from)

        return queryset



