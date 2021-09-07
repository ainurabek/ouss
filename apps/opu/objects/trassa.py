# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.db.models import Q
from apps.accounts.permissions import IsPervichkaOnly
from apps.opu.circuits.serializers import CircuitTrassaList
from apps.opu.circuits.service import create_circuit_transit
from apps.opu.objects.serializers import PGListSerializer, TransitCreateSerializer, \
    TransitDetailSerializer, BridgeListSerializer
from apps.opu.circuits.models import Circuit, CircuitTransit
from apps.opu.circuits.serializers import CircuitList
from apps.opu.objects.models import Object, Point, Transit, Bridge
from apps.opu.objects.serializers import PointList, ObjectListSerializer
from apps.opu.objects.services import check_circuit_transit


class PointListTrassa(ListAPIView):
    """Список ИП для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all().order_by('point').values('id', 'point', 'name')
    serializer_class = PointList


class SelectPointView(APIView):
    """Выбор ИП для фильтрацы ЛП"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        point = Point.objects.get(pk=pk)
        lps = Object.objects.filter(Q(point1=point) | Q(point2=point), id_parent=None)
        serializer = ObjectListSerializer(lps, many=True).data
        return Response(serializer)


class ObjectList(APIView):
    """Список ПГ, ВГ итд"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        childs = obj.parents.all()
        serializer = ObjectListSerializer(childs, many=True).data
        return Response(serializer)


'''Создание трассы для каналов'''
class PGCircuitListView(APIView):
    """Выбор PG для создания трассы circuits"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        childs = obj.parents.all()
        pg = []
        while childs:
            newchilds = []
            for c in childs:
                if c.type_of_trakt.name == 'ПГ':
                    pg.append(c)
                newchilds += c.parents.all()
            childs = newchilds
        serializer = PGListSerializer(pg, many=True).data
        return Response(serializer)


class SelectCircuitView(APIView):
    """Выбор каналы для фильтрацы каналов"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        circuits = Circuit.objects.filter(object=obj)
        serializer = CircuitTrassaList(circuits, many=True).data
        return Response(serializer)


class CircuitListTrassa(ListAPIView):
    """Список circuits для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Circuit.objects.all().order_by('num_circuit')
    serializer_class = CircuitList


class TransitCreateAPIView(CreateAPIView):
    queryset = Transit.objects.all()
    serializer_class = TransitCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_trassa = set(Object.objects.get(id=pk) for pk in request.data["trassa"])
        if self.request.data["create_circuit_transit"]:
            if not check_circuit_transit(new_trassa):
                return Response({"detail": "Транзит провести нельзя, оконечный объект трассы участвует в транзите"},
                                status=status.HTTP_403_FORBIDDEN)
            for obj in new_trassa:
                for bridge in obj.bridges.filter(transit__create_circuit_transit=True):
                    bridge.transit.create_circuit_transit = False
                    bridge.transit.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        bridge = set(self.request.data["can_see"])
        for obj_id in bridge:
            Bridge.objects.create(object_id=obj_id, transit=instance)
        create_circuit_transit(instance)


class RetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Transit.objects.all()
    lookup_field = "pk"
    serializer_class = TransitCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TransitDetailSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        prev_trassa = set(instance.trassa.all())
        new_trassa = set(Object.objects.get(id=pk) for pk in self.request.data["trassa"])
        deleted_object = prev_trassa - new_trassa

        if self.request.data["create_circuit_transit"]:
            if not check_circuit_transit(deleted_object):
                return Response({
                    "detail": "Подчиненные каналы состоят в трассах, которые выходят за рамки расформировываемого."},
                    status=status.HTTP_403_FORBIDDEN)

            if not check_circuit_transit(new_trassa):
                return Response({"detail": "Транзит провести нельзя, оконечный объект трассы участвует в транзите"},
                                status=status.HTTP_403_FORBIDDEN)
            added_object = new_trassa - prev_trassa

            for obj in added_object:
                for bridge in obj.bridges.filter(transit__create_circuit_transit=True):
                    bridge.transit.create_circuit_transit = False
                    bridge.transit.save()

        trassa = serializer.save()
        trassa.can_see.all().delete()
        bridge = self.request.data["can_see"]

        for obj_id in bridge:
            Bridge.objects.create(object_id=obj_id, transit=trassa)

        if self.request.data["create_circuit_transit"]:
            create_circuit_transit(trassa)
            for deleted_object in prev_trassa - set(trassa.trassa.all()):
                for circuit in deleted_object.circuit_object_parent.all():
                    circuit_transit = CircuitTransit.objects.create()
                    circuit_transit.trassa.add(circuit)
                    circuit.trassa = circuit_transit
                    circuit.is_modified = False
                    circuit.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.create_circuit_transit:
            for obj in instance.trassa.all().iterator():
                for circuit in obj.circuit_object_parent.all():
                    circuit_transit = CircuitTransit.objects.create()
                    circuit_transit.trassa.add(circuit)
                    circuit.trassa = circuit_transit
                    circuit.is_modified = False
                    circuit.save()
        instance.delete()


class TransitListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = get_object_or_404(Object, pk=pk)
        serializer = BridgeListSerializer(obj.bridges.all(), many=True)
        return Response(serializer.data)
