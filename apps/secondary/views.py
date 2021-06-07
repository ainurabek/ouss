from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, get_object_or_404, UpdateAPIView
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.secondary.models import TypeStation, SecondaryBase
from apps.secondary.serializers import TypeStationSerializer, SecondaryBaseSerializer, SecondaryBaseCreateSerializer
from apps.accounts.permissions import IsVtorichkaOnly, SuperUser, IngenerUser
from apps.opu.objects.models import Outfit, Point
from apps.opu.objects.serializers import PointList


class TypeStationModelViewSet(ModelViewSet):
    serializer_class = TypeStationSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = TypeStation.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsVtorichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]

class PointsByOutfittView(APIView):
        authentication_classes = (TokenAuthentication,)
        search_fields = ('name',)
        serializer = PointList

        def get(self, request, pk):
            outfit = get_object_or_404(Outfit, pk=pk)
            points = Point.objects.filter(id_outfit = outfit)
            serializer = PointList(points, many=True).data
            return Response(serializer)


class BaseModelView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = SecondaryBase.objects.all().order_by('outfit').prefetch_related('point', 'outfit', 'type_station')
    lookup_field = 'pk'
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('outfit', 'point')

    def get_serializer_class(self):
        if self.action == 'list':
            return SecondaryBaseSerializer
        else:
            return SecondaryBaseCreateSerializer
    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsVtorichkaOnly | SuperUser, IngenerUser | SuperUser]
        return [permission() for permission in permission_classes]
