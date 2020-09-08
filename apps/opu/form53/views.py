from django.shortcuts import redirect, render, get_object_or_404
from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status
from apps.opu.form53.serializers import Form53CreateSerializer, Form53Serializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from apps.opu.form51.models import Region
from apps.opu.form53.serializers import Region53Serializer
from apps.accounts.permissions import IsOpuOnly
from apps.opu.form53.services import create_photo_for_form53
from apps.opu.services import PhotoDeleteMixin


# API
#############################################################################################


class Form53CreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    """Создания Формы 5.3"""
    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form53.objects.filter(circuit=circuit).exists():
            content = {'По такому каналу уже форма5.3 создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = Form53CreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, created_by=self.request.user.profile)
            create_photo_for_form53(model=Form53, model_photo=Schema53Photo,
                                    obj=data, field_name="schema", request=request)
            create_photo_for_form53(model=Form53, model_photo=Order53Photo,
                                    obj=data, field_name="order", request=request)

            for i in circuit.transit.all():
                if circuit != i:
                    form53 = Form53.objects.create(
                        circuit=i, comments= data.comments
                    )
                    form53.schema53_photo.add(*data.schema53_photo.all())
                    form53.order53_photo.add(*data.order53_photo.all())
            for i in circuit.transit2.all():
                if circuit != i:
                    form53 = Form53.objects.create(
                        circuit=i, comments=data.comments
                    )
                    form53.schema53_photo.add(*data.schema53_photo.all())
                    form53.order53_photo.add(*data.order53_photo.all())
            response = {"data": "Форма 5.3 создана успешно"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Form53ListAPIView(ListAPIView):
    """Список Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form53Serializer

    def get_queryset(self):
        queryset = Form53.objects.all()
        region = self.request.query_params.get('region', None)
        customer = self.request.query_params.get('customer', None)
        category = self.request.query_params.get('category', None)
        circuit = self.request.query_params.get('circuit', None)

        if region is not None and region != "":
            queryset = queryset.filter(circuit__id_object__id_outfit__outfit=region)
        if customer is not None and customer != "":
            queryset = queryset.filter(circuit__customer=customer)
        if category is not None and category != "":
            queryset = queryset.filter(circuit__category=category)
        if circuit is not None and circuit != "":
            queryset = queryset.filter(circuit__name=circuit)
        return queryset



class Form53UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form53.objects.all()
    serializer_class = Form53CreateSerializer


class Form53DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form53


class Region53ListAPIView(ListAPIView):
    """Список Регоинов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = Region53Serializer


class Order53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        create_photo_for_form53(model=Form53, model_photo=Order53Photo,
                                obj=form53, field_name="order", request=request)
        response = {"data": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Order53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model_for_delete = Order53Photo


class Schema53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        create_photo_for_form53(model=Form53, model_photo=Schema53Photo,
                                obj=form53, field_name="schema", request=request)
        response = {"data": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Schema53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model_for_delete = Schema53Photo
