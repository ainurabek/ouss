from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import Http404
from apps.opu.objects.models import Object, TPO, Outfit, Point, IP, TypeOfTrakt
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from apps.opu.objects.serializers import LPSerializer, TPOSerializer, \
    OutfitListSerializer, OutfitCreateSerializer, PointListSerializer, PointCreateSerializer, \
    ObjectSerializer, LPCreateSerializer, \
    ObjectCreateSerializer, IPCreateSerializer, SelectObjectSerializer, PointList, ObjectListSerializer, \
    ObjectFilterSerializer, TraktListSerializer
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import xlwt
from django.db.models import Q
from apps.opu.circuits.models import Circuit
from apps.opu.objects.models import Category
from apps.opu.form51.models import Form51
from apps.opu.form_customer.models import Form_Customer
from apps.opu.objects.serializers import LPEditSerializer

from apps.opu.objects.serializers import LPDetailSerializer


class TPOListView(viewsets.ModelViewSet):
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'index')
    filterset_fields = ('name', 'index')

    def export_csv(request):
        if 'csv' in request.GET:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="tpo.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('TPO')
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['ID', 'Название', 'Индекс']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            rows = TPO.objects.all()
            if 'name' in request.GET and request.GET.get('name', None):
                rows = rows.filter(name=request.GET.get('name'))
            if 'index' in request.GET and request.GET.get('index', None):
                rows = rows.filter(tpo=request.GET['index'])

            for row in rows:
                row_num += 1
                item = []
                item.append(row.id)
                item.append(row.name)
                item.append(row.index)
                for col_num in range(len(item)):
                    ws.write(row_num, col_num, item[col_num], font_style)
            wb.save(response)
            return response


class TPOCreateView(generics.CreateAPIView):
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer


class TPOEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = TPO.objects.all()
    serializer_class = TPOSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


# class TPODeleteView(generics.DestroyAPIView):
#     queryset = Outfit.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


# Предприятия
class OutfitsListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Outfit.objects.all()
    lookup_field = 'pk'
    serializer_class = OutfitListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('outfit', 'adding', 'tpo__index', 'tpo__name', 'num_outfit', 'type_outfit__name')
    filterset_fields = ('outfit', 'adding', 'tpo', 'num_outfit', 'type_outfit')


class OutfitCreateView(generics.CreateAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitCreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class OutfitEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Outfit.objects.all()
    serializer_class = OutfitCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


# class OutfitDeleteView(generics.DestroyAPIView):
#     queryset = Outfit.objects.all()
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


# ИПы
class PointListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
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


class PointEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Point.objects.all()
    serializer_class = PointCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# class PointDeleteView(generics.DestroyAPIView):
#     queryset = Point.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


class IPCreateView(APIView):

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
    permission_classes = (IsAuthenticated,)


'''
Линии передачи
'''


class LPListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class LPEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Object.objects.all()
    serializer_class = LPEditSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


# class LPDeleteView(generics.DestroyAPIView):
#     queryset = Object.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


class ObjectListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit')

    def get(self, request, pk):
        lp = get_object_or_404(Object, pk=pk)
        trakt = Object.objects.filter(id_parent=lp.pk)
        data = TraktListSerializer(trakt, many=True).data
        return Response(data)


class ObjectDetailView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

# ПГ ВГ ТГ ЧГ РГ


class ObjectCreateView(APIView):
    """"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        parent = get_object_or_404(Object, pk=pk)
        data = request.data
        name = data['name']
        serializer = ObjectCreateSerializer(data=data)

        if parent.type_of_trakt is not None:
            if parent.type_of_trakt.name == 'ВГ':
                type_obj = TypeOfTrakt.objects.get(name='ПГ')
                request.data["type_of_trakt"] = type_obj.pk
            elif parent.type_of_trakt.name == 'ТГ':
                type_obj = TypeOfTrakt.objects.get(name='ВГ')
                request.data["type_of_trakt"] = type_obj.pk
            elif parent.type_of_trakt.name == 'ЧГ':
                type_obj = TypeOfTrakt.objects.get(name='ТГ')
                request.data["type_of_trakt"] = type_obj.pk
            elif parent.type_of_trakt.name == 'РГ':
                type_obj = TypeOfTrakt.objects.get(name='ЧГ')
                request.data["type_of_trakt"] = type_obj.pk

        if serializer.is_valid():
            instance=serializer.save(
                id_parent=parent,
                type_line=parent.type_line,
                id_outfit=parent.id_outfit,
                our=parent.our,
                created_by=self.request.user.profile,
                point1=parent.point1,
                name=parent.name+'-'+name,


            )

            if data['amount_channels'] == '12':
                for x in range(1, 13):
                    Circuit.objects.create(name=parent.name+ "-" + name + '/' + str(x),
                                                     id_object=instance,
                                                     num_circuit = x,
                                                     category=Category.objects.get(id=instance.category.id),
                                                     point1=Point.objects.get(id=instance.point1.id),
                                                     point2=Point.objects.get(id=instance.point2.id),
                                                     created_by=request.user.profile)
            elif data['amount_channels'] == '30':
                for x in range(1, 31):
                    Circuit.objects.create(name=parent.name+ "-" + name + '/' + str(x),
                                                     id_object=instance,
                                                     num_circuit = x,
                                                     category=Category.objects.get(id=instance.category.id),
                                                     point1=Point.objects.get(id=instance.point1.id),
                                                     point2=Point.objects.get(id=instance.point2.id),
                                                     created_by=request.user.profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectEditView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        list = []
        obj = get_object_or_404(Object, pk=pk)
        list.append(obj.name)
        serializer = ObjectCreateSerializer(obj, data=request.data)
        if serializer.is_valid():
            instance=serializer.save()
            if list[0] != instance.name:
                circuits = Circuit.objects.filter(id_object=instance)
                all = Circuit.objects.filter(id_object=instance).count()+1
                cir = 1
                for circuit in circuits:
                    if cir <= all:
                        circuit.name=Circuit.objects.filter(pk=circuit.id).update(name=instance.id_parent.name+('-')+instance.name+"/"+str(cir))
                        cir += 1

            elif obj.point1 != instance.point1 or obj.point2 != instance.point2:
                circuits = Circuit.objects.filter(id_object=instance.id)
                all = Circuit.objects.filter(id_object=instance.id).count() + 1

                for circuit in circuits:
                    all -= 1
                    circuit.name = Circuit.objects.filter(pk=circuit.id).update(
                        point1=instance.point1.id,
                        point2=instance.point2.id)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, instance, validated_data):
        Circuit.objects.filter(id_object=instance.id).update(point1= validated_data.get('point1', instance.point1),
                                                             point2= validated_data.get('point2', instance.point2))

        return instance



class SelectObjectView(APIView):
    """Выбор ЛП для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

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


class ObjectList(APIView):
    """Список ПГ, ВГ итд"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        objs = Object.objects.filter(id_parent=pk)
        serializer = ObjectListSerializer(objs, many=True).data
        return Response(serializer)


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
            

            for cir in main_obj.circ_obj.all():
                name = obj.name + "/" + str(cir.num_circuit)
                try:
                    circuit = Circuit.objects.get(name=name)
                except ObjectDoesNotExist:
                    break
                cir.transit.add(circuit)

        return Response(status=status.HTTP_201_CREATED)


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

            for cir in main_obj.circ_obj.all():
                name = obj.name + "/" + str(cir.num_circuit)
                try:
                    circuit = Circuit.objects.get(name=name)
                except ObjectDoesNotExist:
                    break
                cir.transit2.add(circuit)

        return Response(status=status.HTTP_201_CREATED)


class SaveTrassaView(APIView):
    """Сохранение трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        main_obj = Object.objects.get(pk=pk)
        for i in main_obj.transit.all():
            if main_obj.transit.all() not in i.transit.all():
                i.transit.add(*main_obj.transit.all())
            if main_obj.transit2.all() not in i.transit2.all():
                i.transit2.add(*main_obj.transit2.all())

        for i in main_obj.transit2.all():
            if main_obj.transit2.all() not in i.transit2.all():
                i.transit2.add(*main_obj.transit2.all())
            if main_obj.transit.all() not in i.transit.all():
                i.transit.add(*main_obj.transit.all())

        for cir in main_obj.circ_obj.all():
            for obj in main_obj.transit.all():
                name = obj.name + "/" + str(cir.num_circuit)
                try:
                    name = Circuit.objects.get(name=name)
                except ObjectDoesNotExist:
                    break
                name.transit.add(*cir.transit.all())
                name.transit2.add(*cir.transit2.all())

        for cir in main_obj.circ_obj.all():
            for obj in main_obj.transit2.all():
                name = obj.name + "/" + str(cir.num_circuit)
                try:
                    name = Circuit.objects.get(name=name)
                except ObjectDoesNotExist:
                    break
                name.transit2.add(*cir.transit2.all())
                name.transit.add(*cir.transit.all())
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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def delete(self, request, main_pk, pk):
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
                name = obj.name + "/" + cir.num_circuit
                try:
                    name = Circuit.objects.get(name=name)
                    cir.transit.remove(name)
                except ObjectDoesNotExist:
                    pass

        if main_obj.transit2.filter(pk=pk).exists():
            main_obj.transit2.remove(obj)

            for cir in main_obj.circ_obj.all():
                name = obj.name + "/" + cir.num_circuit
                try:
                    name = Circuit.objects.get(name=name)
                    cir.transit2.remove(name)
                except ObjectDoesNotExist:
                    pass

        for t_obj in main_obj.transit.all():
            if t_obj.transit.filter(pk=pk).exists():
                t_obj.transit.remove(obj)

                for circ in t_obj.circ_obj.all():
                    name = obj.name + "/" + circ.num_circuit
                    try:
                        name = Circuit.objects.get(name=name)
                        if circ.transit.filter(pk=name.pk).exists():
                            circ.transit.remove(name)
                    except ObjectDoesNotExist:
                        pass

        for t_obj in main_obj.transit2.all():
            if t_obj.transit2.filter(pk=pk).exists():
                t_obj.transit2.remove(obj)

                for circ in t_obj.circ_obj.all():
                    name = obj.name + "/" + circ.num_circuit
                    try:
                        name = Circuit.objects.get(name=name)
                        if circ.transit2.filter(pk=name.pk).exists():
                            circ.transit2.remove(name)
                    except ObjectDoesNotExist:
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
        ip = self.request.query_params.get('ip', None)

        if tpo is not None and tpo != '':
            queryset = queryset.filter(Q(tpo1__index=tpo) | Q(tpo2__index=tpo))
        if point is not None and point != '':
            queryset = queryset.filter(Q(point1__point=point) | Q(point2__point=point))
        if outfit is not None and outfit != '':
            queryset = queryset.filter(id_outfit__outfit=outfit)
        if ip is not None and ip != '':
            queryset = queryset.filter(Q(destination1__point_id__point__icontains=ip) | Q(destination2__point_id__point__icontains=ip))

        return queryset