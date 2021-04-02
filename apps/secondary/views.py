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

from apps.secondary.models import TypeStation
from apps.secondary.serializers import TypeStationSerializer
from apps.accounts.permissions import IsVtorichkaOnly, SuperUser, IngenerUser


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