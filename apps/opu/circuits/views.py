from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from apps.opu.circuits.serializers import CircuitEdit, CircuitDetail, CircuitUpdateSerializer, \
    TransitCircSerializer
from rest_framework import generics, status
from apps.opu.circuits.models import Circuit, CircuitTransit
from rest_framework.views import APIView
from apps.accounts.permissions import IsPervichkaOnly, IngenerUser, SuperUser
from apps.opu.circuits.service import get_circuit_diff, update_trassa_for_new_circuit, create_new_trassa, check_modified
from apps.opu.circuits.service import update_circuit_active
from apps.opu.objects.models import Object

from apps.opu.form_customer.serializers import CircuitFormList


class CircuitListViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        circuits = Object.objects.get(pk=pk).circ_obj.all().prefetch_related('point1', 'point2', 'object', 'id_object',
                                                                             'customer', 'category')
        serializer = CircuitFormList(circuits, many=True)
        return Response(serializer.data)


class CircuitEditView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser)

    def perform_update(self, serializer):
        instance = serializer.save(created_by=self.request.user.profile)
        update_circuit_active(object=instance.object)


class CircuitDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitDetail
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CircuitHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

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


class AddCircuitTrassa(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, circuit_pk, transit_pk):
        circuit = get_object_or_404(Circuit, pk=circuit_pk)
        transit = get_object_or_404(CircuitTransit, pk=transit_pk)
        if circuit.trassa == transit:
            return Response([], status=status.HTTP_200_OK)
        response = [TransitCircSerializer(cir).data for cir in circuit.trassa.trassa.all()]
        return Response(response, status=status.HTTP_200_OK)


class DeleteCircuitTrassa(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, circuit_pk, transit_pk):
        circuit = get_object_or_404(Circuit, pk=circuit_pk)
        transit = get_object_or_404(CircuitTransit, pk=transit_pk)
        not_modified_circuit = circuit.object.circuit_object_parent.filter(is_modified=False).first()
        if not circuit or transit.obj_trassa == not_modified_circuit.trassa.obj_trassa:
            return Response([], status=status.HTTP_200_OK)
        response = []

        for obj in not_modified_circuit.trassa.obj_trassa.trassa.all():
            try:
                response.append(TransitCircSerializer(obj.circuit_object_parent.get(num_circuit=circuit.num_circuit)))
            except ObjectDoesNotExist:
                pass

        return Response(response, status=status.HTTP_200_OK)


class UpdateCircuitAPIView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
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

        self.perform_update(serializer)
        update_trassa_for_new_circuit(instance, new_circuit_in_trassa)
        create_new_trassa(circuit_for_delete_in_trassa)
        check_modified(instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
