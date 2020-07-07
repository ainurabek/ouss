from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from apps.opu.circuits.serializers import CircuitList, CircuitEdit
from rest_framework import permissions, viewsets, status, generics
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response

from apps.opu.objects.models import Object
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# class CircuitViewSet(viewsets.ModelViewSet):
#     queryset = Circuit.objects.all()
#     serializer_class = CircuitList
#     lookup_field = 'pk'
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticatedOrReadOnly,)
from apps.accounts.permissions import IsOpuOnly


class CircuitListViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('num_circuit', 'name', 'type_using', 'category', 'num_order', 'date_order',
                     'num_arenda', 'speed', 'measure', 'point1', 'point2', 'customer', 'id_object', 'mode', 'type_com')
    filterset_fields = ('point1', 'point2', 'customer', 'id_object', 'category')

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        trakt = self.get_object(pk)
        circuit = Circuit.objects.filter(id_object=trakt.pk)
        data = CircuitList(circuit, many=True).data
        return Response(data)


class CircuitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)

