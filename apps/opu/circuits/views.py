from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.opu.circuits.serializers import CircuitList, CircuitEdit, CircuitDetail
from rest_framework import generics, status
from apps.opu.circuits.models import Circuit
from rest_framework.views import APIView
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import ListWithPKMixin
from apps.opu.circuits.service import get_circuit_diff
from apps.opu.circuits.service import update_circuit_active



class CircuitListViewSet(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    model = Circuit
    serializer = CircuitList
    field_for_filter = "id_object"
    order_by = 'id'


class CircuitEditView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        instance = serializer.save(created_by=self.request.user.profile)
        update_circuit_active(object=instance.object)

class CircuitDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitDetail
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

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
