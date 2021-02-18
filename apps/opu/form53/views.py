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

from apps.accounts.permissions import IsPervichkaOnly

from apps.opu.services import PhotoDeleteMixin
from apps.opu.form53.services import get_form53_diff
from apps.opu.services import create_photo


class Form53CreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    """Создания Формы 5.3"""
    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form53.objects.filter(circuit=circuit).exists():
            content = {'detail':'По такому каналу уже форма5.3 создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = Form53CreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, created_by=self.request.user.profile)
            create_photo(model=Form53, model_photo=Schema53Photo,
                                    obj=data, field_name="schema", request=request)
            create_photo(model=Form53, model_photo=Order53Photo,
                                    obj=data, field_name="order", request=request)

            #мы 4 января удалили возможность создавать форму 5.3 для транзитов в канале.
            #Теперь будет создаваться форма 5.3 только для основного канала, который выбрали

            response = {"message": "Форма 5.3 создана успешно"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Form53ListAPIView(ListAPIView):
    """Список Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form53Serializer

    def get_queryset(self):
        queryset = Form53.objects.all().prefetch_related('order53_photo', 'schema53_photo', 'circuit')
        outfit = self.request.query_params.get('outfit', None)
        customer = self.request.query_params.get('customer', None)
        pg_object = self.request.query_params.get('pg_object', None)

        if outfit is not None:
            queryset = queryset.filter(circuit__object__id_outfit=outfit)
        if customer is not None:
            queryset = queryset.filter(circuit__customer=customer)

        #добавили в фильтр поиск по ПГ, у которых есть каналы

        if pg_object is not None:
            queryset = queryset.filter(circuit__object=pg_object)

        return queryset


class Form53UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    queryset = Form53.objects.all()
    serializer_class = Form53CreateSerializer


class Form53DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    queryset = Form53


class Order53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        create_photo(model=Form53, model_photo=Order53Photo,
                                obj=form53, field_name="order", request=request)
        response = {"message": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Order53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    model_for_delete = Order53Photo


class Schema53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        create_photo(model=Form53, model_photo=Schema53Photo,
                                obj=form53, field_name="schema", request=request)
        response = {"message": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Schema53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    model_for_delete = Schema53Photo


class Form53History(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        form53 = Form53.objects.get(pk=pk)
        histories = form53.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_form53_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)