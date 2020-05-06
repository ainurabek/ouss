from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404

# Create your views here.
from apps.opu.objects.models import Object, TPO, Outfit, Point, IP
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from apps.opu.objects.serializers import LPSerializer, TPOSerializer, \
    OutfitListSerializer, OutfitCreateSerializer, PointListSerializer, PointCreateSerializer, IPListSerializer,\
    ObjectSerializer, LPCreateSerializer, \
    ObjectCreateSerializer, IPCreateSerializer
from rest_framework import permissions, viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import xlwt

from django.db.models import Q
from django.utils import timezone


# TPO
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


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def tpo_delete_view(request, tpo_id):
    try:
        tpo = TPO.objects.get(id=tpo_id)
    except tpo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = tpo.delete()
        data = {}
        if operation:
            data["success"] = "TPO успешно удален"
        else:
            data["failure"] = "TPO не удален"
        return Response(data=data)


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


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def outfit_delete_view(request, outfit_id):
    outfit = Outfit.objects.get(id=outfit_id)
    try:
        outfit
    except outfit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = outfit.delete()
        data = {}
        if operation:
            data["success"] = "Предприятие успешно удалено"
        else:
            data["failure"] = "Предприятие не удалено"
        return Response(data=data)


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


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def point_delete_view(request, pk):
    point = Point.objects.get(id=pk)
    try:
        point
    except point.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = point.delete()
        data = {}
        if operation:
            data["success"] = "Point успешно удален"
        else:
            data["failure"] = "Point не удален"
        return Response(data=data)


class IPListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = IP.objects.all()
    lookup_field = 'pk'
    serializer_class = IPListSerializer


class IPCreateView(generics.CreateAPIView):
    queryset = IP.objects.all()
    serializer_class = IPCreateSerializer


class IPEditView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = IP.objects.all()
    serializer_class = IPCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def ip_delete_view(request, pk):
    ip = IP.objects.get(id=pk)
    try:
        ip
    except ip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = ip.delete()
        data = {}
        if operation:
            data["success"] = "ИП успешно удален"
        else:
            data["failure"] = "ИП не удален"
        return Response(data=data)


'''
Линии передачи
'''


class LPListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(id_parent=None)
    lookup_field = 'pk'
    serializer_class = LPSerializer


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
    serializer_class = LPCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user.profile)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def lp_delete_view(request, pk):
    lp = Object.objects.get(id=pk)
    try:
        lp
    except lp.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation = lp.delete()
        data = {}
        if operation:
            data["success"] = "Линия передачи успешно удалена"
        else:
            data["failure"] = "Линия передачи не удалена"
        return Response(data=data)


class TraktListView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    pass


class ObjectListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit')

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        lp = self.get_object(pk)
        trakt = Object.objects.filter(id_parent=lp.pk)
        data = ObjectSerializer(trakt, many=True).data
        return Response(data)


# for obj in objects:
#     if obj.type_of_trakt.id==2 or 3 or 4 or 5 or 6: #ПГ
#         print(objects)
#         return HttpResponse(objects)
#     else:
#         return HttpResponse("у этой линии передачи нет тракта")


# ПГ ВГ ТГ ЧГ РГ

class ObjectCreateView(APIView):
    """"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        parent = self.get_object(pk)
        serializer = ObjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                id_parent=parent,
                type_line=parent.type_line,
                id_outfit=parent.id_outfit,
                our=parent.our,
                created_by=self.request.user.profile
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObjectEditView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Object.objects.get(pk=pk)
        except Object.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ObjectCreateSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def trassa(request):
    data = []
    objects = Object.objects.all()
    for obj in objects:
        data.append({'ip1': obj.point1, 'name': obj.name, 'ip2': obj.point2, 'id_transit1': [], 'id_transit2': []})
        if obj.id_transit1 != None:
            data.append({'id_transit1': obj.id_transit1})
        elif obj.id_transit2 != None:
            data.append({'id_transit2': obj.id_transit2})
    return JsonResponse({'data': data})


def select_lp(request, main_pk):
    main_obj = Object.objects.get(pk=main_pk)
    ip_ot = Object.objects.filter(Q(point1=main_obj.point1) | Q(point2=main_obj.point1))
    ip_ot = ip_ot.filter(id_parent=None)
    ip_do = Object.objects.filter(Q(point1=main_obj.point2) | Q(point2=main_obj.point2))
    ip_do = ip_do.filter(id_parent=None)

    trassa_list1 = main_obj.transit.all().reverse()
    trassa_list2 = main_obj.transit2.all()

    response = {
        'main_obj': main_obj.to_json(),
        'trassa_list1': [m.to_json() for m in trassa_list1],
        'trassa_list2': [m.to_json() for m in trassa_list2],
        'ip_ot': [m.to_json() for m in ip_ot],
        'ip_do': [m.to_json() for m in ip_do]
    }

    return JsonResponse(response)


def select_object(request, lp_pk):
    objects = Object.objects.filter(id_parent=lp_pk)

    response = {
        'objects': [m.to_json() for m in objects],
    }
    return JsonResponse(response)


def left_trassa(request, pk, id):
    main_obj = Object.objects.get(pk=pk)
    obj = Object.objects.get(pk=id)

    if main_obj.transit.filter(pk=id).exists():
        pass
    else:
        main_obj.transit.add(obj)
        Object.objects.filter(pk=id).update(maker_trassa=request.user.profile)

    response = {
        'main_obj': main_obj.to_json(),
        'obj': obj.to_json(),
    }
    return redirect('apps:objects:select_lp', main_pk=main_obj.pk)


def right_trassa(request, pk, id):
    main_obj = Object.objects.get(pk=pk)
    obj = Object.objects.get(pk=id)

    if main_obj.transit2.filter(pk=id).exists():
        pass
    else:
        main_obj.transit2.add(obj)
        Object.objects.filter(pk=id).update(maker_trassa=request.user.profile)

    response = {
        'main_obj': main_obj.to_json(),
        'obj': obj.to_json(),
    }

    return redirect('apps:objects:select_lp', main_pk=main_obj.pk)


def save_trassa(request, pk):
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

    response = {'success': 'Трасса создано успешно'}

    return JsonResponse(response)


def delete_trassa(request, main_pk, pk):
    main_obj = Object.objects.get(pk=main_pk)
    obj = Object.objects.get(pk=pk)

    if main_obj.transit.filter(pk=id).exists():
        main_obj.transit.remove(obj)
        obj.transit2.clear()
        obj.transit.clear()

    if main_obj.transit2.filter(pk=id).exists():
        main_obj.transit2.remove(obj)
        obj.transit2.clear()
        obj.transit.clear()

    response = {'success': 'Объект удалена успешно'}

    return JsonResponse(response)