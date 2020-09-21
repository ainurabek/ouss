from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication
import datetime
from datetime import date

from apps.analysis.serializers import DispEvent1ListSerializer
from apps.dispatching.models import Event


class DispEvent1ListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=True)
    lookup_field = 'pk'
    serializer_class = DispEvent1ListSerializer

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.queryset.filter(created_at=today,  index1__id=8, callsorevent=False)

        responsible_outfit = self.request.query_params.get('responsible_outfit', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if responsible_outfit is not None and responsible_outfit != '':
            queryset = self.queryset.filter(responsible_outfit=responsible_outfit, index1__id=8)
        if date_to == "" and date_from != '':
            queryset = self.queryset.filter(created_at=date_from, index1__id=8)
        elif date_to != '' and date_from == '':
            queryset = self.queryset.filter(created_at=date_to, index1__id=8)
        elif date_to != '' and date_from != '':
            queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to, index1__id=8)

        return queryset


