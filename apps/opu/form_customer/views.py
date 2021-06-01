from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status, viewsets
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView
from apps.opu.customer.models import Customer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.opu.form_customer.models import Form_Customer, OrderCusPhoto
from apps.opu.form_customer.serializers import FormCustomerCreateSerializer, FormCustomerSerializer, \
    CircuitListSerializer, SignalizationSerializer, PointSerializer
from apps.opu.form_customer.serializers import CustomerFormSerializer
from apps.opu.form_customer.serializers import ObjectFormCustomer
from apps.opu.objects.models import Object, Point
from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from apps.opu.services import PhotoDeleteMixin, PhotoCreateMixin, ListWithPKMixin, create_photo
from apps.opu.form_customer.service import get_form_customer_diff
from apps.opu.form_customer.models import Signalization

from apps.logging.form_customer.views import FormCustomerCircuitLogUtil, \
    FormCustomerObjectLogUtil, FormCustomerIPLogUtil


class SignalizationView(viewsets.ModelViewSet):
    queryset = Signalization.objects.all().order_by('name')
    serializer_class = SignalizationSerializer
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser]
        return [permission() for permission in permission_classes]
    def perform_create(self, serializer):
        instance = serializer.save()



class CustomerFormListView(ListAPIView):
    """Список арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerFormSerializer
    queryset = Customer.objects.all()


class FormCustomerListAPIView(ListAPIView):
    """ Фильтрация Формы арендаторов  по арендаторам """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('object', 'circuit', 'object__customer', 'circuit__customer', 'customer')
    queryset = Form_Customer.objects.defer('created_by').select_related('signalization', 'point1', 'point2').\
        prefetch_related('circuit__trassa__trassa', 'object__bridges__transit__trassa', 'order_cust_photo')
    serializer_class = FormCustomerSerializer

class PointListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class CircuitListAPIView(APIView, ListWithPKMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Circuit
    serializer = CircuitListSerializer
    field_for_filter = "customer_id"


class ObjectListAPIView(APIView, ListWithPKMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Object
    serializer = ObjectFormCustomer
    field_for_filter = "customer_id"



class FormCustomerCircCreateAPIView(APIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form_Customer.objects.filter(circuit=circuit).exists():
            content = {'detail':'По такому каналу уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(circuit=circuit, created_by=self.request.user.profile)
            instance.save()
            FormCustomerCircuitLogUtil(self.request.user, instance.pk).obj_create_action('form_customer_circuit_created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCustomerObjCreateAPIView(APIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def post(self, request, pk):
        object = get_object_or_404(Object, pk=pk)
        if Form_Customer.objects.filter(object=object).exists():
            content = {'detail': 'По такому обьекту уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(object=object, created_by=self.request.user.profile)
            instance.save()
            FormCustomerObjectLogUtil(self.request.user, instance.pk).obj_create_action(
                'form_customer_object_created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormCustomerIPCreateAPIView(APIView):
    """Создания Формы арендаторов через ИПы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def post(self, request, pk1, pk2, customer_id):
        point1 = get_object_or_404(Point, pk=pk1)
        point2 = get_object_or_404(Point, pk=pk2)
        customer = get_object_or_404(Customer, pk = customer_id)
        if Form_Customer.objects.filter(point1=point1, point2=point2).exists():
            content = {'detail': 'С такими ИПами уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(point1=point1, point2=point2, customer=customer, created_by=self.request.user.profile)
            instance.save()
            FormCustomerIPLogUtil(self.request.user, instance.pk, instance.pk).obj_create_action(
                'form_customer_ip_created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormCustomerUpdateAPIView(UpdateAPIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form_Customer.objects.all()
    serializer_class = FormCustomerCreateSerializer


class FormCustomerDeleteAPIView(DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form_Customer.objects.all()


class OrderCusPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    model = Form_Customer
    model_photo = OrderCusPhoto
    search_field_for_img = "order"

    def post(self, request, pk):
        form_cus = Form_Customer.objects.get(pk=pk)
        for img in request.FILES.getlist('order'):
            OrderCusPhoto.objects.create(src=img, form_customer=form_cus)
        response = {"detail": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class OrderCusPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model_for_delete = OrderCusPhoto


class FormCustomerHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def get(self, request, pk):
        form_customer = Form_Customer.objects.get(pk=pk)
        histories = form_customer.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_form_customer_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)
