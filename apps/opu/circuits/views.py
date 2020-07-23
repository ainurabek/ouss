from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from apps.opu.circuits.serializers import CircuitList, CircuitEdit
from rest_framework import generics
from apps.opu.circuits.models import Circuit
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# class CircuitViewSet(viewsets.ModelViewSet):
#     queryset = Circuit.objects.all()
#     serializer_class = CircuitList
#     lookup_field = 'pk'
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticatedOrReadOnly,)
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import ListWithPKMixin


class CircuitListViewSet(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('num_circuit', 'name', 'type_using', 'category', 'num_order', 'date_order',
                     'num_arenda', 'speed', 'measure', 'point1', 'point2', 'customer', 'id_object', 'mode', 'type_com')
    filterset_fields = ('point1', 'point2', 'customer', 'id_object', 'category')
    model = Circuit
    serializer = CircuitList
    field_for_filter = "id_object"


class CircuitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)

