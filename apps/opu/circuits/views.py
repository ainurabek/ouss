from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from apps.opu.circuits.serializers import CircuitList, CircuitEdit, CircuitDetail, CircuitUpdateSerializer
from rest_framework import generics, status
from apps.opu.circuits.models import Circuit, CircuitTransit
from rest_framework.views import APIView
from apps.accounts.permissions import IsPervichkaOnly, IngenerUser, SuperUser
from apps.opu.circuits.service import get_circuit_diff, valid_for_deleted, valid_for_add, update_trassa_for_new_circuit, \
    create_new_trassa, check_modified
from apps.opu.circuits.service import update_circuit_active
from apps.opu.objects.models import Object

from apps.opu.form_customer.serializers import CircuitFormList


class CircuitListViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        circuits = Object.objects.get(pk=pk).circ_obj.all().prefetch_related('point1', 'point2', 'object', 'id_object', 'customer',
                                                                         'category')
        serializer = CircuitFormList(circuits, many=True)
        return Response(serializer.data)


class CircuitEditView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser)

    def perform_update(self, serializer):
        circuit = self.get_object()
        flag = bool(circuit.first)
        if flag:
            if circuit.object.type_line.main_line_type.name == 'КЛС':
                circuit.point1.total_point_channels_KLS -= 1
                circuit.point1.save()
                circuit.point2.total_point_channels_KLS -= 1
                circuit.point2.save()
            elif circuit.object.type_line.main_line_type.name == 'ЦРРЛ':
                circuit.point1.total_point_channels_RRL -= 1
                circuit.point1.save()
                circuit.point2.total_point_channels_RRL -= 1
                circuit.point2.save()
        instance = serializer.save(created_by=self.request.user.profile)
        if instance.first:
            if circuit.object.type_line.main_line_type.name == 'КЛС':
                circuit.point1.total_point_channels_KLS += 1
                circuit.point1.save()
                circuit.point2.total_point_channels_KLS += 1
                circuit.point2.save()

            elif circuit.object.type_line.main_line_type.name == 'ЦРРЛ':
                circuit.point1.total_point_channels_RRL += 1
                circuit.point1.save()
                circuit.point2.total_point_channels_RRL += 1
                circuit.point2.save()
        update_circuit_active(object=instance.object)


class CircuitDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitDetail
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CircuitHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

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


class UpdateCircuitAPIView(UpdateAPIView):
    queryset = CircuitTransit.objects.all()
    serializer_class = CircuitUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        prev_trassa = set(instance.trassa.all())
        new_trassa = set(Circuit.objects.get(id=pk) for pk in self.request.data["trassa"])
        circuit_for_delete_in_trassa = prev_trassa - new_trassa
        new_circuit_in_trassa = new_trassa - prev_trassa

        if not valid_for_deleted(instance.obj_trassa, circuit_for_delete_in_trassa):
            return Response({"detail": "Порядок транзита не позволяет провести рассоединение"},
                            status=status.HTTP_403_FORBIDDEN)

        if not valid_for_add(new_circuit_in_trassa):
            return Response({"detail": "Транзит провести нельзя, объект трассы участвует в другом транзите"},
                            status=status.HTTP_403_FORBIDDEN)

        self.perform_update(serializer)
        update_trassa_for_new_circuit(instance, new_circuit_in_trassa)
        create_new_trassa(circuit_for_delete_in_trassa)
        check_modified(instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
