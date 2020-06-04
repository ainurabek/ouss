from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
from apps.opu.circuits.serializers import CircuitList, CircuitEdit
from rest_framework import permissions, viewsets, status, generics
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response

from apps.opu.objects.models import Object
from rest_framework.views import APIView


class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = CircuitList
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

class CircuitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Circuit.objects.all()
    serializer_class = CircuitEdit
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)