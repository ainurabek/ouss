from django.shortcuts import redirect, render, get_object_or_404

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
    CircuitListSerializer, SignalizationSerializer
from apps.opu.form_customer.serializers import CustomerFormSerializer
from apps.opu.form_customer.serializers import ObjectFormCustomer
from apps.opu.objects.models import Object
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import PhotoDeleteMixin, PhotoCreateMixin, ListWithPKMixin, create_photo
from apps.opu.form_customer.service import get_form_customer_diff
from apps.opu.form_customer.models import Signalization
#API
#######################################################################################################################



class SignalizationView(viewsets.ModelViewSet):
    queryset = Signalization.objects.all().order_by('name')
    serializer_class = SignalizationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    filterset_fields = ('object', 'circuit', 'customer',)
    queryset = Form_Customer.objects.all()
    serializer_class = FormCustomerSerializer


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
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form_Customer.objects.filter(circuit=circuit).exists():
            content = {'По такому каналу уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, customer=circuit.customer, created_by=self.request.user.profile)
            create_photo(model=Form_Customer, model_photo=OrderCusPhoto, obj=data, field_name="src", request=request)
            response = {"data": "Форма арендатора успешно создана"}
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCustomerObjCreateAPIView(APIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        object = get_object_or_404(Object, pk=pk)
        if Form_Customer.objects.filter(object=object).exists():
            content = {'По такому обьекту уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(object=object, customer=object.customer, created_by=self.request.user.profile)
            create_photo(model=Form_Customer, model_photo=OrderCusPhoto, obj=data, field_name="order", request=request)
            response = {"data": "Форма арендатора успешно создана"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCustomerUpdateAPIView(UpdateAPIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form_Customer.objects.all()
    serializer_class = FormCustomerCreateSerializer


class FormCustomerDeleteAPIView(DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form_Customer.objects.all()


class OrderCusPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    model = Form_Customer
    model_photo = OrderCusPhoto
    search_field_for_img = "order"

    def post(self, request, pk):
        form_cus = Form_Customer.objects.get(pk=pk)
        for img in request.FILES.getlist('order'):
            OrderCusPhoto.objects.create(src=img, form_customer=form_cus)
        response = {"data": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class OrderCusPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model_for_delete = OrderCusPhoto

class FormCustomerHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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