from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.opu.circuits.serializers import CircuitList, CircuitEdit, MeasureCircSerializer, SpeedSerializer, \
    TypeComSerializer, ModeCircSerializer
from rest_framework import generics, status
from apps.opu.circuits.models import Circuit, Measure, Speed, TypeCom, Mode
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import ListWithPKMixin
from django.http import JsonResponse

# from apps.opu.objects.services import get_active_channels, get_total_amount_active_channels

from apps.opu.objects.models import Object

from apps.opu.circuits.service import get_circuit_diff

# from apps.opu.objects.services import update_circuit_fisrt
from apps.opu.circuits.service import create_circuit

from apps.opu.circuits.service import update_circuit_active


class CircuitListViewSet(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('num_circuit', 'name', 'type_using', 'category', 'num_order',
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
        instance = serializer.save(created_by=self.request.user.profile)
        update_circuit_active(object=instance.object)


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


class CircuitHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        histories = circuit.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_circuit_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)
