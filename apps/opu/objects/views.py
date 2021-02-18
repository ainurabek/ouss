from django.http import JsonResponse
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
    ObjectCreateSerializer, IPCreateSerializer, ObjectListSerializer, \
    ObjectFilterSerializer, TraktListSerializer, AllObjectSerializer, TypeOfTraktSerializer, TypeOfLocationSerializer, \
    LineTypeSerializer, AmountChannelListSerializer, ConsumerSerializer, BugSerializer
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.opu.objects.serializers import LPEditSerializer
from apps.opu.objects.serializers import LPDetailSerializer
from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from apps.opu.objects.services import get_type_of_trakt, check_parent_type_of_trakt, save_old_object, \
    update_circuit, update_total_amount_channels
from apps.opu.services import PhotoCreateMixin, PhotoDeleteMixin, get_object_diff, \
get_ip_diff, get_point_diff, get_outfit_diff
from apps.opu.objects.services import adding_an_object_to_trassa
from apps.opu.circuits.service import create_circuit
from apps.opu.objects.serializers import ObjectEditSerializer, MainLineTypeListSerializer
from apps.opu.objects.models import OrderObjectPhoto, MainLineType
from apps.opu.objects.services import create_form51
from apps.opu.customer.models import Customer
from apps.opu.objects.services import update_total_point_channels
from apps.opu.objects.serializers import LineTypeCreateSerializer


class TPOListView(viewsets.ModelViewSet):
    queryset = TPO.objects.all().order_by('name')
    serializer_class = TPOSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'index')
    filterset_fields = ('name', 'index')

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class AmountChannelListAPIView(viewsets.ModelViewSet):
    queryset = AmountChannel.objects.all().order_by('value')
    serializer_class = AmountChannelListSerializer
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class TypeTraktListView(viewsets.ModelViewSet):
    queryset = TypeOfTrakt.objects.all().order_by('-id')
    serializer_class = TypeOfTraktSerializer
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class OutfitsListView(viewsets.ModelViewSet):
    """Предприятия"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsPervichkaOnly,)
    queryset = Outfit.objects.all().order_by('id').prefetch_related('tpo', 'type_outfit')
    lookup_field = 'pk'
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('outfit', 'adding', 'tpo__index', 'tpo__name', 'num_outfit', 'type_outfit__name')
    filterset_fields = ('outfit', 'adding', 'tpo', 'num_outfit', 'type_outfit')

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return OutfitListSerializer
        else:
            return OutfitCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class PointListView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all().order_by('point').prefetch_related('tpo', 'id_outfit')
    lookup_field = 'pk'
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('point', 'name', 'tpo__index', 'tpo__name', 'id_outfit__outfit', 'id_outfit__adding',
                     'region', 'type_equipment')
    filterset_fields = ('point', 'name', 'tpo', 'id_outfit', 'region', 'type_equipment')

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PointListSerializer
        else:
            return PointCreateSerializer


class IPCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)


class LPListView(viewsets.ModelViewSet):
    """ Линии передачи """
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(id_parent=None).order_by('name').prefetch_related('transit',
                                                                                       'transit2', 'reserve_transit',
                                                                                       'reserve_transit2', 'point1',
                                                                                       'point2')
    lookup_field = 'pk'
    serializer_class = LPSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'point1__point', 'point2__point')

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

    def perform_update(self, serializer):
        instance = serializer.save(created_by=self.request.user.profile)
        instance.save()


class ObjectAllView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all().order_by('name').prefetch_related('tpo1', 'tpo2',
                                                                      'point1', 'point2', 'transit', 'transit2',
                                                                      'id_outfit', 'category', 'customer')
    serializer_class = AllObjectSerializer


#we use this view in form 5.3
class PGObjectView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.filter(type_of_trakt__name='ПГ').order_by('name').prefetch_related('point1', 'point2',
                                                                                                 'type_of_trakt')
    lookup_field = 'pk'
    serializer_class = ObjectListSerializer


class ObjectListView(APIView):
    authentication_classes = (TokenAuthentication,)
    search_fields = ('name',)
    serializer = TraktListSerializer

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        childs = obj.parents.all()
        serializer = TraktListSerializer(childs, many=True).data
        return Response(serializer)


class ObjectDetailView(RetrieveDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
        instance = self.get_object()
        self.perform_destroy(instance)
        update_total_amount_channels(instance=instance)
        response = {"message": "Объект успешно удален"}
        return Response(response, status=status.HTTP_204_NO_CONTENT)


# ПГ ВГ ТГ ЧГ РГ
class ObjectCreateView(APIView):
    """"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)

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


class FilterObjectList(ListAPIView):
    """Фильтрация объектов. Выходят и points, ips по запросу ИП"""
    serializer_class = ObjectFilterSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = Object.objects.all().prefetch_related('point1', 'point2', 'id_outfit', 'ip_object', 'consumer')
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
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class MainLineTypeList(ListAPIView):
    """Список главных типов линии"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = MainLineType.objects.all().order_by('name')
    serializer_class = MainLineTypeListSerializer


class LineTypeAPIVIew(ModelViewSet):
    serializer_class = LineTypeSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = LineType.objects.all().order_by('name')

    def get_serializer_class(self):
        if self.action == 'list':
            return LineTypeSerializer
        else:
            return LineTypeCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class CategoryAPIVIew(ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = Category.objects.all().order_by('index')

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class ConsumerModelViewSet(ModelViewSet):
    serializer_class = ConsumerSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = Consumer.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]


class ObjectHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

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
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    search_field_for_img = "object_order"
    model = Object
    model_photo = OrderObjectPhoto


class OrderObjectFileDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model = Object
    model_for_delete = OrderObjectPhoto


# for dashboard
def get_points_amount(request):
    points_amount = Point.objects.count()
    return JsonResponse(points_amount, safe=False)


def get_tpo_amount(request):
    tpo_amount = TPO.objects.count()
    return JsonResponse(tpo_amount, safe=False)


def get_outfits_amount(request):
    outfits_amount = Outfit.objects.count()
    return JsonResponse(outfits_amount, safe=False)


def get_customers_amount(request):
    customers_amount = Customer.objects.count()
    return JsonResponse(customers_amount, safe=False)


class BugModelViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all().order_by('-id')
    serializer_class = BugSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)
