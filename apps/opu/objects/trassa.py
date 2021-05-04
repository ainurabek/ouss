# coding: utf-8
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.db.models import Q
from apps.accounts.permissions import IsPervichkaOnly
from apps.opu.circuits.serializers import CircuitTrassaList
from apps.opu.circuits.service import create_circuit_transit
from apps.opu.objects.serializers import PGListSerializer, TransitCreateSerializer, \
    TransitDetailSerializer
from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import CircuitList
from apps.opu.objects.models import Object, Point, Transit, Bridge
from apps.opu.objects.serializers import PointList, ObjectListSerializer


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

    def perform_create(self, serializer):
        instance = serializer.save()
        bridge = self.request.data["can_see"]

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

    def perform_update(self, serializer):
        trassa = serializer.save()
        trassa.can_see.all().delete()
        bridge = self.request.data["can_see"]

        for obj_id in bridge:
            Bridge.objects.create(object_id=obj_id, transit=trassa)
        create_circuit_transit(trassa)
