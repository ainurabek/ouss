# coding: utf-8
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response

from apps.logging.models import ActivityLogModel

from apps.accounts.permissions import IsPervichkaOnly, SuperUser

from apps.logging.serializers import ActivityLogSerializer
from django.db.models import Q




class ActivityLogAPIVIew(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  IsPervichkaOnly | SuperUser)
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        queryset = ActivityLogModel.objects.all()
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from is not None and date_from != '' and date_to is not None and date_to != '':
            q1 = queryset.filter(action_time__date__gte=date_from)
            queryset = q1.filter(action_time__date__lte=date_to)
        return queryset.order_by('-action_time')