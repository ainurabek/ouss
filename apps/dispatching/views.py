import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import EventListSerializer, CircuitEventList, ObjectEventSerializer, IPSSerializer
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object, IP

from .serializers import EventCreateSerializer, EventDetailSerializer
from rest_framework import viewsets

now = datetime.datetime.now()
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from django.views.generic import ListView
from .forms import EventForm
from .models import Event, TypeOfJournal
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

#API

class EventListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.all()
    lookup_field = 'pk'
    serializer_class = EventListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('type_journal', 'contact_name',
                        'reason', 'index1', 'index2', 'responsible_outfit', 'send_from')

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == "retrieve":
            return EventDetailSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        date_from_from = self.request.query_params.get('date_from_from', None)
        date_to_from = self.request.query_params.get('date_to_from', None)
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
            serializer.save(ips=ip, created_by=self.request.user.profile, created_at=now)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CircuitEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Circuit.objects.all()
    serializer_class = CircuitEventList
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('id_object', 'customer', 'name', 'type_using')

class EventCircuitCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""

    def post(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(circuit=circuit, created_by=self.request.user.profile, created_at=now)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObjectEventListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectEventSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('name', 'point1', 'point2', 'id_outfit', 'customer')

class EventObjectCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    """Создания Event"""

    def post(self, request, pk):
        object = Object.objects.get(pk=pk)
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(object=object, created_by=self.request.user.profile, created_at=now)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventUpdateAPIView(UpdateAPIView):
    """Редактирования event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

class EventDeleteAPIView(DestroyAPIView):
    """Удаления event"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    lookup_field = 'pk'


