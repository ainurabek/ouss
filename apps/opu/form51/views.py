from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView

from apps.opu.form51.models import Form51, Region
from apps.opu.form51.serializers import Form51CreateSerializer, Form51Serializer, RegionSerializer, \
    Form51ReserveSerializer
from apps.opu.objects.models import Object
# Templates
from apps.opu.form51.models import SchemaPhoto, OrderPhoto
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import PhotoDeleteMixin, PhotoCreateMixin, ListWithPKMixin, create_photo




# API
#############################################################################################



class FormCreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    """Создания Формы 5.1"""

    def post(self, request, pk):
        obj = get_object_or_404(Object, pk=pk)
        serializer = Form51CreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save(object=obj, created_by=request.user.profile)
            create_photo(model=Form51, model_photo=SchemaPhoto, obj=data, field_name="schema", request=request)
            create_photo(model=Form51, model_photo=OrderPhoto, obj=data, field_name="order", request=request)

            for i in obj.transit.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=data.customer,
                        num_ouss=data.num_ouss,
                        order=data.order, schema=data.schema,
                        reserve=data.reserve
                    )

            for i in obj.transit2.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=data.customer,
                        num_ouss=data.num_ouss,
                        order=data.order, schema=data.schema,
                        reserve=data.reserve
                    )
            response = {"data": "Форма 5.1 создана успешно"}
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormListAPIView(ListAPIView):
    """Список Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form51Serializer

    def get_queryset(self):
        queryset = Form51.objects.all()
        region = self.request.query_params.get('region', None)
        customer = self.request.query_params.get('customer', None)

        if region is not None and region != "":
            queryset = queryset.filter(object__id_outfit__outfit=region)
        if customer is not None and customer != "":
            queryset = queryset.filter(customer__customer=customer)

        return queryset


class Form51UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form51.objects.all()
    serializer_class = Form51CreateSerializer


class Form51DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form51.objects.all()


class RegionListAPIView(ListAPIView):
    """Список Регоинов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ReserveDetailAPIView(APIView, ListWithPKMixin):
    """ Резерв """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Form51
    serializer = Form51ReserveSerializer
    field_for_filter = "pk"


class ReserveDelete(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def delete(self, request, form_pk, reserve_pk):
        form51 = get_object_or_404(Form51, pk=form_pk)
        obj = get_object_or_404(Object, pk=reserve_pk)
        if form51.reserve_object.filter(pk=reserve_pk).exists():
            form51.reserve_object.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model = Form51
    model_photo = OrderPhoto
    search_field_for_img = "order"


class OrderPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model = Form51
    model_for_delete = OrderPhoto


class SchemaPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model = Form51
    model_photo = SchemaPhoto
    search_field_for_img = "schema"


class SchemaPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model = Form51
    model_for_delete = SchemaPhoto
