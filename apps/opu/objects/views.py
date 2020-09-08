from django.http import HttpResponse
from apps.opu.objects.models import Object, TPO, Outfit, Point, IP
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from apps.opu.objects.serializers import LPSerializer, TPOSerializer, \
    OutfitListSerializer, OutfitCreateSerializer, PointListSerializer, PointCreateSerializer, \
    ObjectSerializer, LPCreateSerializer, \
    ObjectCreateSerializer, IPCreateSerializer, SelectObjectSerializer, PointList, ObjectListSerializer, \
    ObjectFilterSerializer, TraktListSerializer, AllObjectSerializer
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.opu.circuits.models import Circuit
from apps.opu.form51.models import Form51
from apps.opu.form_customer.models import Form_Customer
from apps.opu.objects.serializers import LPEditSerializer
from apps.opu.objects.serializers import LPDetailSerializer
from apps.opu.objects.serializers import IPSerializer
from apps.accounts.permissions import IsOpuOnly
from apps.opu.objects.services import get_type_of_trakt, check_parent_type_of_trakt, create_circuit, save_old_object, \
    update_circuit, update_amount_channels, cascading_delete_object
from apps.opu.services import ListWithPKMixin


class TPOListView(viewsets.ModelViewSet):
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'index')
    filterset_fields = ('name', 'index')


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
    authentication_classes = (TokenAuthentication,)
    queryset = Outfit.objects.all()
    lookup_field = 'pk'
    serializer_class = OutfitListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('outfit', 'adding', 'tpo__index', 'tpo__name', 'num_outfit', 'type_outfit__name')
    filterset_fields = ('outfit', 'adding', 'tpo', 'num_outfit', 'type_outfit')


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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all()
    lookup_field = 'pk'
    serializer_class = PointListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit')


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


class IPListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = IP.objects.all()
    lookup_field = 'pk'
    serializer_class = IPSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('point_id', 'object_id', 'tpo_id')


""" Линии передачи """


class LPListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(id_parent=None)
    lookup_field = 'pk'
    serializer_class = LPSerializer

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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class LPEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Object.objects.all()
    serializer_class = LPEditSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class ObjectAllView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    lookup_field = 'pk'
    serializer_class = AllObjectSerializer


class ObjectListView(APIView, ListWithPKMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit')
    model = Object
    serializer = TraktListSerializer
    field_for_filter = "id_parent"


class ObjectDetailView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        update_amount_channels(obj=instance)       
        self.perform_destroy(instance)
#         cascading_delete_object(instance)
        response = {"data": "Объект успешно удален"}
        return Response(response, status=status.HTTP_204_NO_CONTENT)



# ПГ ВГ ТГ ЧГ РГ


class ObjectCreateView(APIView):
    """"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        parent = get_object_or_404(Object, pk=pk)
        serializer = ObjectCreateSerializer(data=request.data)

        if check_parent_type_of_trakt(parent):
            type_obj = get_type_of_trakt(parent)
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

            create_circuit(model=Circuit, obj=instance, request=request)
            update_amount_channels(obj=instance)
            response = {"data": "Объект успешно создан"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectEditView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def put(self, request, pk):
        obj = get_object_or_404(Object, pk=pk)
        old_obj = save_old_object(obj)

        serializer = ObjectCreateSerializer(obj, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            update_circuit(model=Circuit, old_obj=old_obj, obj=instance)
            response = {"data": "Объект успешно отредактирован"}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectObjectView(APIView):
    """Выбор ЛП для создания трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        serializer = SelectObjectSerializer(obj).data
        return Response(serializer)


class PointListTrassa(ListAPIView):
    """Список ИП для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all()
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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if main_obj.transit.filter(pk=pk).exists():
            pass
        else:
            main_obj.transit.add(obj)
            Object.objects.filter(pk=pk).update(maker_trassa=request.user.profile)

            num_circuit = main_obj.circ_obj.count() if main_obj.circ_obj.count() <= obj.circ_obj.count() else \
                obj.circ_obj.count()
            if num_circuit != 0:

                for cir in main_obj.circ_obj.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                    cir.transit.add(circuit)
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class CreateRightTrassaView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if main_obj.transit2.filter(pk=pk).exists():
            pass
        else:
            main_obj.transit2.add(obj)
            Object.objects.filter(pk=pk).update(maker_trassa=request.user.profile)

            num_circuit = main_obj.circ_obj.count() if main_obj.circ_obj.count() <= obj.circ_obj.count() else\
                obj.circ_obj.count()

            if num_circuit != 0:

                for cir in main_obj.circ_obj.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                    cir.transit2.add(circuit)
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveTrassaView(APIView):
    """Сохранение трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        main_obj = get_object_or_404(Object, pk=pk)
        for i in main_obj.transit.all():
            i.transit.add(*main_obj.transit.all())
            i.transit2.add(*main_obj.transit2.all())

        for i in main_obj.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
            i.transit.add(*main_obj.transit.all())


        for cir in main_obj.circ_obj.all():
            for obj in main_obj.transit.all():
                if obj.circ_obj.count() == 0:
                    continue
                try:
                    circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit.add(*cir.transit.all())
                circuit.transit2.add(*cir.transit2.all())

        for cir in main_obj.circ_obj.all():
            for obj in main_obj.transit2.all():
                if obj.circ_obj.count() == 0:
                    continue
                try:
                    circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit2.add(*cir.transit2.all())
                circuit.transit.add(*cir.transit.all())
        response = {"data": "Трасса успешно сахранен"}
        return Response(status=status.HTTP_201_CREATED)

    def post(self, request, pk):
        main_obj = Object.objects.get(pk=pk)
        data=request.data
        if data['save_in'] == True:
            if Form51.objects.filter(object=main_obj).exists():
                return HttpResponse("В форме 5.1. уже есть такая трасса")
            else:
                Form51.objects.create(object=main_obj)
        elif data['save_in'] == False:
            pass
        if data['customer'] == True:
            if Form_Customer.objects.filter(object=main_obj).exists():
                return HttpResponse("В форме арендаторов уже есть такая трасса")
            else:
                Form_Customer.objects.create(object=main_obj, customer=main_obj.customer)
        elif data['customer'] == False:
            pass
        return Response(status=status.HTTP_201_CREATED)


class DeleteTrassaView(APIView):
    """Удаления трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            main_obj = Object.objects.get(pk=main_pk)

            if main_obj.transit.filter(pk=pk).exists():
                main_obj.transit.remove(main_obj)

                for cir in main_obj.circ_obj.all():
                    cir.transit.remove(cir)

            if main_obj.transit2.filter(pk=pk).exists():
                main_obj.transit2.remove(main_obj)

                for cir in main_obj.circ_obj.all():
                    cir.transit2.remove(cir)

            all_cir = main_obj.circ_obj.count()

            for t_obj in main_obj.transit.all():
                if t_obj.transit.filter(pk=pk).exists():
                    t_obj.transit.remove(main_obj)

                    for circ in t_obj.circ_obj.all():
                        if all_cir < int(circ.num_circuit):
                            break
                        circuit = main_obj.circ_obj.all()[int(circ.num_circuit)-1]
                        if circ.transit.filter(pk=circuit.pk).exists():
                            circ.transit.remove(circuit)

            for t_obj in main_obj.transit2.all():
                if t_obj.transit2.filter(pk=pk).exists():
                    t_obj.transit2.remove(main_obj)

                    for circ in t_obj.circ_obj.all():
                        if all_cir < int(circ.num_circuit):
                            break
                        circuit = main_obj.circ_obj.all()[int(circ.num_circuit)-1]
                        if circ.transit2.filter(pk=circuit.pk).exists():
                            circ.transit2.remove(circuit)

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            main_obj = Object.objects.get(pk=main_pk)
            obj = Object.objects.get(pk=pk)

            obj.transit2.clear()
            obj.transit.clear()

            for cir in obj.circ_obj.all():
                cir.transit.clear()
                cir.transit2.clear()

            if main_obj.transit.filter(pk=pk).exists():
                main_obj.transit.remove(obj)

                for cir in main_obj.circ_obj.all():
                    try:
                        circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                        cir.transit.remove(circuit)
                    except IndexError:
                        pass

            if main_obj.transit2.filter(pk=pk).exists():
                main_obj.transit2.remove(obj)

                for cir in main_obj.circ_obj.all():
                    try:
                        circuit = obj.circ_obj.all()[int(cir.num_circuit)-1]
                        cir.transit2.remove(circuit)
                    except IndexError:
                        pass

            for t_obj in main_obj.transit.all():
                if t_obj.transit.filter(pk=pk).exists():
                    t_obj.transit.remove(obj)

                    for circ in t_obj.circ_obj.all():
                        try:
                            circuit = obj.circ_obj.all()[int(circ.num_circuit)-1]
                            if circ.transit.filter(pk=circuit.pk).exists():
                                circ.transit.remove(circuit)
                        except IndexError:
                            pass

            for t_obj in main_obj.transit2.all():
                if t_obj.transit2.filter(pk=pk).exists():
                    t_obj.transit2.remove(obj)

                    for circ in t_obj.circ_obj.all():
                        try:
                            circuit = obj.circ_obj.all()[int(circ.num_circuit)-1]
                            if circ.transit2.filter(pk=circuit.pk).exists():
                                circ.transit2.remove(circuit)
                        except IndexError:
                            pass

            return Response(status=status.HTTP_204_NO_CONTENT)


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


        if tpo is not None and tpo != '':
            queryset = queryset.filter(Q(tpo1__index=tpo) | Q(tpo2__index=tpo))
        if point is not None and point != '':
            queryset = queryset.filter(Q(point1__point=point) | Q(point2__point=point))
        if outfit is not None and outfit != '':
            queryset = queryset.filter(id_outfit__outfit=outfit)

        return queryset