# coding: utf-8

from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet

from apps.opu.circuits.serializers import CategorySerializer
from apps.opu.objects.models import Object, TPO, Outfit, Point, IP, TypeOfTrakt, TypeOfLocation, LineType, \
    Category, AmountChannel, Consumer, Bug

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from apps.opu.objects.serializers import LPSerializer, TPOSerializer, \
    OutfitListSerializer, OutfitCreateSerializer, PointListSerializer, PointCreateSerializer, \
    ObjectSerializer, LPCreateSerializer, \
    ObjectCreateSerializer, IPCreateSerializer, SelectObjectSerializer, PointList, ObjectListSerializer, \
    ObjectFilterSerializer, TraktListSerializer, AllObjectSerializer, TypeOfTraktSerializer, TypeOfLocationSerializer, \
    LineTypeSerializer, AmountChannelListSerializer, ConsumerSerializer, BugSerializer

from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.opu.form_customer.models import Form_Customer
from apps.opu.objects.serializers import LPEditSerializer
from apps.opu.objects.serializers import LPDetailSerializer
from apps.accounts.permissions import IsOpuOnly
from apps.opu.objects.services import get_type_of_trakt, check_parent_type_of_trakt, save_old_object, \
    update_circuit, update_total_amount_channels
from apps.opu.services import ListWithPKMixin, PhotoCreateMixin, PhotoDeleteMixin, get_object_diff, \
get_ip_diff, get_point_diff, get_outfit_diff
from apps.opu.objects.services import adding_an_object_to_trassa
from apps.opu.circuits.service import create_circuit
from apps.opu.objects.serializers import ObjectEditSerializer
from apps.opu.objects.models import OrderObjectPhoto
from apps.opu.objects.services import create_form51
from apps.opu.customer.models import Customer
from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import CircuitList

from apps.opu.objects.services import update_total_point_channels

from apps.opu.circuits.serializers import CircuitTrassaList


class BugModelViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all().order_by('-id')
    serializer_class = BugSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class AmountChannelListAPIView(viewsets.ModelViewSet):
    queryset = AmountChannel.objects.all().order_by('value')
    serializer_class = AmountChannelListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class TPOListView(viewsets.ModelViewSet):
    queryset = TPO.objects.all().order_by('name')
    serializer_class = TPOSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'index')
    filterset_fields = ('name', 'index')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


# for dashboard
def get_points_amount(request):
    points_amount = Point.objects.all().count()
    return JsonResponse(points_amount, safe=False)


def get_tpo_amount(request):
    tpo_amount = TPO.objects.all().count()
    return JsonResponse(tpo_amount, safe=False)


def get_outfits_amount(request):
    outfits_amount = Outfit.objects.all().count()
    return JsonResponse(outfits_amount, safe=False)


def get_customers_amount(request):
    customers_amount = Customer.objects.all().count()
    return JsonResponse(customers_amount, safe=False)


class TypeTraktListView(viewsets.ModelViewSet):
    queryset = TypeOfTrakt.objects.all().order_by('-id')
    serializer_class = TypeOfTraktSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class TPOCreateView(generics.CreateAPIView):
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class TPOEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)


# Предприятия

class OutfitsListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsOpuOnly,)
    queryset = Outfit.objects.all().order_by('outfit')
    lookup_field = 'pk'
    serializer_class = OutfitListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('outfit', 'adding', 'tpo__index', 'tpo__name', 'num_outfit', 'type_outfit__name')
    filterset_fields = ('outfit', 'adding', 'tpo', 'num_outfit', 'type_outfit')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]
        return [permission() for permission in permission_classes]


class OutfitCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Outfit.objects.all()
    serializer_class = OutfitCreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class OutfitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Outfit.objects.all()
    serializer_class = OutfitCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


# ИПы
class PointListView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all().order_by('point')
    lookup_field = 'pk'
    serializer_class = PointListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding',
                     'region', 'type_equipment')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit', 'region', 'type_equipment')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class PointCreateView(generics.CreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)


class PointEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Point.objects.all()
    serializer_class = PointCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)


class IPCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        request.data["object_id"] = pk
        serializer = IPCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IPDeleteView(generics.DestroyAPIView):
    queryset = IP.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)



""" Линии передачи """


class LPListView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(id_parent=None).order_by('name')
    lookup_field = 'pk'
    serializer_class = LPSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'point1__point', 'point2__point')

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return LPSerializer
        elif self.action == "retrieve":
            return LPDetailSerializer


class LPCreateView(generics.CreateAPIView):
    queryset = Object.objects.all()
    serializer_class = LPCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, *args, **kwargs):
        if Object.objects.filter(name=request.data['name'], point1=request.data['point1'],
                                 point2=request.data['point2']).exists():
            content = {"detail": "Такой обьект уже создан"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = LPCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user.profile)
            # instance.total_amount_channels = instance.amount_channels.value
            instance.save()
            create_form51(obj=instance)
            # create_circuit(instance, self.request)
            adding_an_object_to_trassa(obj=instance)
            response = {"data": "ЛП создана успешно"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LPEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Object.objects.all()
    serializer_class = LPEditSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        instance = serializer.save(created_by=self.request.user.profile)
        instance.save()


class ObjectAllView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = AllObjectSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class PGObjectView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(type_of_trakt__name='ПГ').order_by('name')
    lookup_field = 'pk'
    serializer_class = ObjectListSerializer


class ObjectListView(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)
    search_fields = ('name',)
    model = Object
    serializer = TraktListSerializer
    field_for_filter = "id_parent"
    order_by = 'name'


class ObjectDetailView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (IsOpuOnly, )
        instance = self.get_object()
        self.perform_destroy(instance)
        update_total_amount_channels(instance=instance)
        response = {"message": "Объект успешно удален"}
        return Response(response, status=status.HTTP_204_NO_CONTENT)


# ПГ ВГ ТГ ЧГ РГ


class ObjectCreateView(APIView):
    """"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        parent = get_object_or_404(Object, pk=pk)

        if Object.objects.filter(name=parent.name+'-'+request.data["name"], point1=request.data["point1"], point2=request.data["point2"]).exists():
            content = {"detail": "Такой обьект уже создан"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        serializer = ObjectCreateSerializer(data=request.data)

        if check_parent_type_of_trakt(parent):
            type_obj = get_type_of_trakt(parent)
            # if not request.data._mutable:
            #     request.data._mutable = True
            request.data["type_of_trakt"] = type_obj.pk

        if serializer.is_valid():
            instance = serializer.save(
                id_parent=parent,
                type_line=parent.type_line,
                id_outfit=parent.id_outfit,
                our=parent.our,
                created_by=request.user.profile,
                name=parent.name+'-'+request.data["name"],
            )

            # if instance.type_of_trakt.name == 'ПГ':
            instance.total_amount_channels = instance.amount_channels.value
            instance.save()
            create_form51(obj = instance)
            # create_circuit(obj=instance, request=request)
            adding_an_object_to_trassa(obj=instance)
            update_total_amount_channels(instance=instance)
            create_circuit(instance, self.request)
            update_total_point_channels(instance=instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectEditView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def put(self, request, pk):
        obj = get_object_or_404(Object, pk=pk)
        old_obj = save_old_object(obj)

        serializer = ObjectEditSerializer(obj, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            update_circuit(old_obj=old_obj, obj=instance)
            response = {"message": "Объект успешно отредактирован"}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectObjectView(APIView):
    """Выбор ЛП для создания трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        serializer = SelectObjectSerializer(obj).data
        return Response(serializer)


class PointListTrassa(ListAPIView):
    """Список ИП для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all().order_by('point')
    serializer_class = PointList


class SelectPointView(APIView):
    """Выбор ИП для фильтрацы ЛП"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        point = Point.objects.get(pk=pk)
        lps = Object.objects.filter(Q(point1=point) | Q(point2=point), id_parent=None)
        serializer = ObjectListSerializer(lps, many=True).data
        return Response(serializer)


class ObjectList(APIView, ListWithPKMixin):
    """Список ПГ, ВГ итд"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    model = Object
    serializer = ObjectListSerializer
    field_for_filter = "id_parent"


class CreateLeftTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsOpuOnly)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if not main_obj.transit.filter(pk=pk).exists():
            main_obj.transit.add(*obj.transit2.all().reverse(), *obj.transit.all())

            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()

            Object.objects.filter(pk=pk).update(created_by=request.user.profile)

            num_circuit = main_obj.circuit_object_parent.count() if main_obj.circuit_object_parent.count() \
                                                                    <= obj.circuit_object_parent.count() else \
                obj.circuit_object_parent.count()
            if num_circuit != 0:

                for cir in main_obj.circuit_object_parent.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit.add(*circuit.transit.all(), *circuit.transit2.all())
                    for tr in circuit.transit.all():
                        tr.transit2.clear()
                        tr.transit.clear()
                    for tr in circuit.transit2.all():
                        tr.transit2.clear()
                        tr.transit.clear()

        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class CreateRightTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)
        # if main_pk.is_transit is True or obj.is_transit is True:
        #     message = {"detail": "Создание трассы может привести к перезаписи трассы транзитных каналов"}
        #     return Response(message, status=status.HTTP_403_FORBIDDEN)
        if not main_obj.transit2.filter(pk=pk).exists():
            main_obj.transit2.add(*obj.transit.all().reverse(), *obj.transit2.all())
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
            Object.objects.filter(pk=pk).update(created_by=request.user.profile)

            num_circuit = main_obj.circuit_object_parent.count() if main_obj.circuit_object_parent.count() <=\
                                                                    obj.circuit_object_parent.count() else\
                obj.circuit_object_parent.count()

            if num_circuit != 0:
                for cir in main_obj.circuit_object_parent.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit2.add(*circuit.transit.all(), *circuit.transit2.all())
                    for tr in circuit.transit.all():
                        tr.transit2.clear()
                        tr.transit.clear()
                    for tr in circuit.transit2.all():
                        tr.transit2.clear()
                        tr.transit.clear()
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveTrassaView(APIView):
    """Сохранение трассы"""
    authentication_classes = (TokenAuthentication, IsOpuOnly,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        main_obj = get_object_or_404(Object, pk=pk)
        for i in main_obj.transit.all():
            i.transit.add(*main_obj.transit.all())
            i.transit2.add(*main_obj.transit2.all())

        for i in main_obj.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
            i.transit.add(*main_obj.transit.all())

        for cir in main_obj.circuit_object_parent.all():
            for obj in main_obj.transit.all():
                if obj.circuit_object_parent.count() == 0:
                    continue
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit.add(*cir.transit.all())
                circuit.transit2.add(*cir.transit2.all())

        for cir in main_obj.circuit_object_parent.all():
            for obj in main_obj.transit2.all():
                if obj.circuit_object_parent.count() == 0:
                    continue
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit2.add(*cir.transit2.all())
                circuit.transit.add(*cir.transit.all())
        response = {"message": "Трасса успешно сахранен"}
        return Response(status=status.HTTP_201_CREATED)

    def post(self, request, pk):
        main_obj = Object.objects.get(pk=pk)
        data = request.data
        if data['customer'] == True:
            if Form_Customer.objects.filter(object=main_obj).exists():
                return HttpResponse("В форме арендаторов уже есть такая трасса")
            else:
                Form_Customer.objects.create(object=main_obj, customer=main_obj.customer)

        return Response(status=status.HTTP_201_CREATED)


class DeleteTrassaView(APIView):
    """Удаления трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            message = {"detail": "Невозможно удалять выбранный обьект"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        else:
            main_obj = Object.objects.get(pk=main_pk)
            obj = Object.objects.get(pk=pk)

            obj.transit2.clear()
            obj.transit.clear()
            obj.transit.add(obj)

            for cir in obj.circuit_object_parent.all():
                cir.transit.clear()
                cir.transit.add(cir)
                cir.transit2.clear()

            main_obj.transit.remove(obj)

            for cir in main_obj.circuit_object_parent.all():
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit.remove(circuit)
                except IndexError:
                    pass

            main_obj.transit2.remove(obj)

            for cir in main_obj.circuit_object_parent.all():
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit2.remove(circuit)
                except IndexError:
                    pass

            for t_obj in main_obj.transit.all():
                t_obj.transit.remove(obj)
                t_obj.transit2.remove(obj)

                for circ in t_obj.circuit_object_parent.all():
                    try:
                        circuit = obj.circuit_object_parent.all()[int(circ.num_circuit)-1]
                        circ.transit.remove(circuit)
                        circ.transit2.remove(circuit)
                    except IndexError:
                        pass

            for t_obj in main_obj.transit2.all():
                t_obj.transit2.remove(obj)
                t_obj.transit.remove(obj)

                for circ in t_obj.circuit_object_parent.all():
                    try:
                        circuit = obj.circuit_object_parent.all()[int(circ.num_circuit)-1]
                        circ.transit2.remove(circuit)
                        circ.transit.remove(circuit)
                    except IndexError:
                        pass

            return Response(status=status.HTTP_204_NO_CONTENT)

class CircuitListTrassa(ListAPIView):
    """Список circuits для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Circuit.objects.all().order_by('num_circuit')
    serializer_class = CircuitList

class SelectCircuitView(APIView):
    """Выбор каналы для фильтрацы каналов"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        circuits = Circuit.objects.filter(object=obj)
        serializer = CircuitTrassaList(circuits, many=True).data
        return Response(serializer)

#создание трассы для каналов
class CreateLeftCircuitTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsOpuOnly)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Circuit.objects.get(pk=main_pk)
        obj = Circuit.objects.get(pk=pk)

        if not main_obj.transit.filter(pk=pk).exists():
            main_obj.transit.add(*obj.transit2.all().reverse(), *obj.transit.all())
            main_obj.object.is_transit = True
            main_obj.object.save()
            obj.object.is_transit = True
            obj.object.save()
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)

class CreateRightCircuitTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Circuit.objects.get(pk=main_pk)
        obj = Circuit.objects.get(pk=pk)
        if not main_obj.transit2.filter(pk=pk).exists():
            main_obj.transit2.add(*obj.transit.all().reverse(), *obj.transit2.all())
            main_obj.object.is_transit = True
            main_obj.object.save()
            obj.object.is_transit = True
            obj.object.save()
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
        response = {"data": "Канал успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveCircuitTrassaView(APIView):
    """Сохранение трассы for circuits"""
    authentication_classes = (TokenAuthentication, IsOpuOnly,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        main_obj = get_object_or_404(Circuit, pk=pk)
        for i in main_obj.transit.all():
            i.transit.add(*main_obj.transit.all())
            i.transit2.add(*main_obj.transit2.all())
        for i in main_obj.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
            i.transit.add(*main_obj.transit.all())
        return Response(status=status.HTTP_201_CREATED)

class DeleteCircuitTrassaView(APIView):
    """Удаления трассы для канала"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            message = {"detail": "Невозможно удалять выбранный канал"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        else:
            main_obj = Circuit.objects.get(pk=main_pk)
            obj = Circuit.objects.get(pk=pk)
            obj.transit2.clear()
            obj.transit.clear()
            obj.transit.add(obj)
            main_trassa = [*main_obj.object.transit.all(), main_obj.object.transit2.all()]
            circ_trassa = [*[cir.object for cir in main_obj.transit.all()], *[cir.object for cir in main_obj.transit2.all()]]

            is_transit = True
            if main_trassa != circ_trassa:
                main_obj.object.is_transit = False


            main_obj.object.is_transit = is_transit
            main_obj.object.save()
            obj.object.is_transit = is_transit
            obj.object.save()
            for t_obj in main_obj.transit.all():
                t_obj.transit.remove(obj)
                t_obj.transit2.remove(obj)
                t_obj.object.is_transit = is_transit
                t_obj.object.save()
            for t_obj in main_obj.transit2.all():
                t_obj.transit2.remove(obj)
                t_obj.transit.remove(obj)
                t_obj.object.is_transit = is_transit
                t_obj.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


#Выходят и points, ips по запросу ИП
class FilterObjectList(ListAPIView):
    """Фильтрация объектов"""
    serializer_class = ObjectFilterSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = Object.objects.all()
        tpo = self.request.query_params.get('tpo', None)
        point = self.request.query_params.get('point', None)
        outfit = self.request.query_params.get('outfit', None)
        consumer = self.request.query_params.get('consumer', None)

        if tpo is not None and tpo != '':
            queryset = queryset.filter(Q(tpo1__index=tpo) | Q(tpo2__index=tpo))
        if point is not None and point != '':
            queryset1 = queryset.filter(Q(point1=point) | Q(point2=point))
            queryset2 = Object.objects.filter(ip_object__point_id=point)
            queryset = queryset1.union(queryset2)
        if outfit is not None and outfit != '':
            queryset = queryset.filter(id_outfit__outfit=outfit)
        if consumer is not None and consumer != '':
            queryset = queryset.filter(consumer=consumer)

        return queryset.order_by('name')


class TypeOfLocationAPIVIew(ModelViewSet):
    serializer_class = TypeOfLocationSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = TypeOfLocation.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class LineTypeAPIVIew(ModelViewSet):
    serializer_class = LineTypeSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = LineType.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class CategoryAPIVIew(ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = Category.objects.all().order_by('index')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class ConsumerModelViewSet(ModelViewSet):
    serializer_class = ConsumerSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = Consumer.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsOpuOnly]

        return [permission() for permission in permission_classes]


class ObjectHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get(self, request, pk):
        object = Object.objects.get(pk=pk)
        histories = object.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_object_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class IPHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get(self, request, pk):
        ip = IP.objects.get(pk=pk)
        histories = ip.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_ip_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class PointHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get(self, request, pk):
        point = Point.objects.get(pk=pk)
        histories = point.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_point_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class OutfitHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def get(self, request, pk):
        outfit = Outfit.objects.get(pk=pk)
        histories = outfit.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_outfit_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class OrderFileUploader(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    search_field_for_img = "object_order"
    model = Object
    model_photo = OrderObjectPhoto


class OrderObjectFileDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model = Object
    model_for_delete = OrderObjectPhoto

