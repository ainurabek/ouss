from copy import deepcopy
from django.shortcuts import get_object_or_404
from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status
from apps.opu.form53.serializers import Form53CreateSerializer, Form53Serializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from apps.opu.services import PhotoDeleteMixin
from apps.opu.form53.services import get_form53_diff
from apps.opu.services import create_photo
from apps.opu.services import PhotoCreateMixin

from apps.logging.form53.views import Form53LogUtil


class Form53CreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    """Создания Формы 5.3"""
    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form53.objects.filter(circuit=circuit).exists():
            content = {'detail':'По такому каналу уже форма5.3 создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = Form53CreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, created_by=self.request.user.profile)
            Form53LogUtil(self.request.user, data.pk).obj_create_action(
                'form53_created')
            create_photo(model=Form53, model_photo=Schema53Photo,
                                    obj=data, field_name="schema", request=request)
            create_photo(model=Form53, model_photo=Order53Photo,
                                    obj=data, field_name="order", request=request)

            #мы 4 января удалили возможность создавать форму 5.3 для транзитов в канале.
            #Теперь будет создаваться форма 5.3 только для основного канала, который выбрали

            response = {"detail": "Форма 5.3 создана успешно"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Form53ListAPIView(ListAPIView):
#     """Список Формы 5.3"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = Form53Serializer
#
#     def get_queryset(self):
#         queryset = Form53.objects.all().prefetch_related('order53_photo', 'schema53_photo', 'circuit')
#         outfit = self.request.query_params.get('outfit', None)
#         customer = self.request.query_params.get('customer', None)
#         pg_object = self.request.query_params.get('pg_object', None)
#         if outfit is not None:
#             queryset = queryset.filter(circuit__object__id_outfit=outfit)
#         if customer is not None:
#             queryset = queryset.filter(circuit__customer=customer)
#
#         #добавили в фильтр поиск по ПГ, у которых есть каналы
#
#         if pg_object is not None:
#             queryset = queryset.filter(circuit__object=pg_object)
#
#         return queryset.order_by('circuit', 'circuit__object')


class Form53ListAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Form53.objects.all().prefetch_related('order53_photo', 'schema53_photo', 'circuit')
        outfit = self.request.query_params.get('outfit', None)
        customer = self.request.query_params.get('customer', None)
        pg_object = self.request.query_params.get('pg_object', None)
        if outfit is not None:
            queryset = queryset.filter(circuit__object__id_outfit=outfit)
        if customer is not None:
            queryset = queryset.filter(circuit__customer=customer)

        if pg_object is not None:
            queryset = queryset.filter(circuit__object=pg_object)
        queryset = queryset.order_by('circuit', 'circuit__object')
        data = []
        example = {
            'id': None, 'circuit': {
                'id': None, 'name': None,  'num_circuit': None, 'category': {},
                'num_order': None, 'comments': None, 'transit': [], 'transit2': []
            },
            'order53_photo': [], 'schema53_photo': [], 'comments': None, 'object_id': None
        }

        if len(queryset) != 0:
            response_data = deepcopy(example)
            form53 = queryset[0]
            response_data['circuit']['transit'] = [
                {
                    'point1': {'id':obj.point1.id,'point': obj.point1.point, 'name': obj.point1.name},
                    'name': obj.name,
                    'point2': {'id': obj.point2.id,'point': obj.point2.point, 'name': obj.point2.name}}
                for obj in form53.circuit.object.transit.all()
            ]
            response_data['circuit']['transit2'] = [
                {
                    'point1': {'id': obj.point1.id, 'point': obj.point1.point, 'name': obj.point1.name},
                    'name': obj.name,
                    'point2': {'id': obj.point2.id, 'point': obj.point2.point, 'name': obj.point2.name}}
                for obj in form53.circuit.object.transit2.all()
            ]
            response_data['object_id'] = form53.circuit.object.id
            data.append(response_data)

        for i in range(len(queryset)):
            response_data = deepcopy(example)
            form53 = queryset[i]
            if data[-1]['object_id'] != form53.circuit.object.id:
                response_data['circuit']['transit'] = [
                    {
                        'point1': {'id': obj.point1.id, 'point': obj.point1.point, 'name': obj.point1.name},
                        'name': obj.name,
                        'point2': {'id': obj.point2.id, 'point': obj.point2.point, 'name': obj.point2.name}}
                    for obj in form53.circuit.object.transit.all()
                ]
                response_data['circuit']['transit2'] = [
                    {
                        'point1': {'id': obj.point1.id, 'point': obj.point1.point, 'name': obj.point1.name},
                        'name': obj.name,
                        'point2': {'id': obj.point2.id, 'point': obj.point2.point, 'name': obj.point2.name}}
                    for obj in form53.circuit.object.transit2.all()
                ]
                response_data['object_id'] = form53.circuit.object.id
                data.append(response_data)
            response_data = Form53Serializer(form53, context={'request': request}).data
            response_data['object_id'] = form53.circuit.object.id
            data.append(response_data)
        return Response(data, status=status.HTTP_200_OK)


class Form53UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form53.objects.all()
    serializer_class = Form53CreateSerializer


class Form53DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form53


class Order53PhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        for img in request.FILES.getlist('order'):
            Order53Photo.objects.create(src=img, form53=form53)

        response = {"detail": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Order53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model_for_delete = Order53Photo


class Schema53PhotoCreateView(APIView, PhotoCreateMixin ):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def post(self, request, pk):
        form53 = get_object_or_404(Form53, pk=pk)
        for img in request.FILES.getlist('schema'):
            Schema53Photo.objects.create(src=img, form53=form53)
        response = {"detail": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


class Schema53PhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model_for_delete = Schema53Photo


class Form53History(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly, )

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