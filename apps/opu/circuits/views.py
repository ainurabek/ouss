from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from apps.opu.circuits.serializers import CircuitList, CircuitEdit, MeasureCircSerializer, SpeedSerializer, \
    TypeComSerializer, ModeCircSerializer
from rest_framework import generics
from apps.opu.circuits.models import Circuit, Measure, Speed, TypeCom, Mode
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import ListWithPKMixin
from django.http import JsonResponse

from apps.opu.objects.services import get_active_channels, get_total_amount_active_channels

from apps.opu.objects.models import Object


class CircuitListViewSet(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('num_circuit', 'name', 'type_using', 'category', 'num_order', 'date_order',
                     'num_arenda', 'speed', 'measure', 'point1', 'point2', 'customer', 'id_object', 'mode', 'type_com')
    filterset_fields = ('point1', 'point2', 'customer', 'id_object', 'category', )
    model = Circuit
    serializer = CircuitList
    field_for_filter = "id_object"


class CircuitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        a = bool(self.get_object().first)
        instance = serializer.save(created_by=self.request.user.profile)
        if a != instance.first:
            get_total_amount_active_channels(obj=instance.id_object, instance=instance)
        get_active_channels(obj= instance.id_object)





class MeasureAPIView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    serializer_class = MeasureCircSerializer
    lookup_field = 'pk'
    queryset = Measure.objects.all()


class SpeedAPIView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    serializer_class = SpeedSerializer
    lookup_field = 'pk'
    queryset = Speed.objects.all()


class TypeComAPIView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    serializer_class = TypeComSerializer
    lookup_field = 'pk'
    queryset = TypeCom.objects.all()


class ModeAPIView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    serializer_class = ModeCircSerializer
    lookup_field = 'pk'
    queryset = Mode.objects.all()

