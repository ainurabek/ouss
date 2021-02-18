from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from apps.opu.circuits.serializers import CircuitList, CircuitEdit, CircuitDetail
from rest_framework import generics, status
from apps.opu.circuits.models import Circuit
from rest_framework.views import APIView
from apps.accounts.permissions import IsPervichkaOnly
from apps.opu.circuits.service import get_circuit_diff
from apps.opu.circuits.service import update_circuit_active
from apps.opu.objects.models import Object


class CircuitListViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        circuits = Circuit.objects.filter(id_object=pk).prefetch_related('point1', 'point2', 'object', 'transit',
                                                                         'transit2', 'id_object', 'customer',
                                                                         'category')
        serializer = CircuitList(circuits, many=True)
        return Response(serializer.data)


class CircuitEditView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def perform_update(self, serializer):
        instance = serializer.save(created_by=self.request.user.profile)
        update_circuit_active(object=instance.object)


class CircuitDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitDetail
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)


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
