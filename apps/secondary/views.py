from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import copy
from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.secondary.models import TypeStation, SecondaryBase, AmbulanceNumsBase
from apps.secondary.serializers import TypeStationSerializer, SecondaryBaseSerializer, SecondaryBaseCreateSerializer, \
    AmbulBaseCreateSerializer, AmbulBaseSerializer
from apps.accounts.permissions import IsVtorichkaOnly, SuperUser, IngenerUser
from apps.secondary.service import secondary_filter, secondary_distinct, ambul_filter, ambul_distinct
from apps.analysis.service import DictWithRound




class TypeStationModelViewSet(ModelViewSet):
    serializer_class = TypeStationSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    queryset = TypeStation.objects.all().order_by('name')

    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsVtorichkaOnly | SuperUser, IngenerUser | SuperUser]

        return [permission() for permission in permission_classes]



class BaseModelView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = SecondaryBase.objects.all().order_by('point').prefetch_related('point', 'outfit', 'type_station')
    lookup_field = 'pk'
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('outfit', 'point', 'type_station')

    def get_serializer_class(self):
        if self.action == 'list':
            return SecondaryBaseSerializer
        else:
            return SecondaryBaseCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsVtorichkaOnly | SuperUser, IngenerUser | SuperUser]
        return [permission() for permission in permission_classes]

@permission_classes([IsAuthenticated,])
def get_report_secondary(request):

    outfit = request.GET.get("outfit")
    type_station = request.GET.get("type_station")
    point = request.GET.get("point")
    queryset = SecondaryBase.objects.all().order_by('point').prefetch_related('point', 'outfit', 'type_station')
    queryset = secondary_filter(queryset, outfit, type_station, point)
    outfits = secondary_distinct(queryset, 'outfit')

    data = []
    content = DictWithRound({
        'name':None,
        'id': None,
        # 'point': {'id': None, 'point': None, 'name': None},
        # 'outfit': {'id': None, 'outfit': None, 'adding': None},
        'type_station': {'id': None, 'name': None},
        'year_of_launch': None,
        'installed_value': None,
        'active_value': None,
        'active_numbering': None,
        'free_numbering': None, 'GAS_numbering': None, 'GAS_return': None, 'KT_numbering': 0,
        'comments': None, 'color': None, 'administrative_division': None
    })
    total_rep = copy.deepcopy(content)
    for outfit in outfits.iterator():
        total_outfit = copy.deepcopy(content)
        out_data = copy.deepcopy(content)
        out_data['name'] = outfit.outfit.outfit
        out_data['KT_numbering'] = None
        out_data['color'] = "outfit"

        data.append(out_data)
        for second in queryset.filter(outfit=outfit.outfit).iterator():
            second_data = copy.deepcopy(content)
            second_data['id'] = second.id
            second_data['name'] = second.point.name
            # second_data['point']['id'] = second.point.id
            # second_data['point']['point'] = second.point.point
            # second_data['point']['name'] = second.point.name
            second_data['type_station']['id'] = second.type_station.id if second.type_station is not None else ''
            second_data['type_station']['name'] = second.type_station.name if second.type_station is not None else ''
            second_data['year_of_launch'] = second.year_of_launch
            second_data['installed_value'] = second.installed_value
            second_data['active_value'] = second.active_value
            second_data['active_numbering'] = second.active_numbering
            second_data['free_numbering'] = second.free_numbering
            second_data['GAS_numbering'] = second.GAS_numbering
            second_data['GAS_return'] = second.GAS_return
            second_data['comments'] = second.comments
            second_data['administrative_division'] = second.administrative_division
            second_data['KT_numbering'] = second.KT_numbering
            data.append(second_data)
            total_outfit['KT_numbering'] += second_data['KT_numbering']
        total_outfit['name'] = 'ИТОГО за ПРЕДПРИЯТИЕ:'
        total_outfit['color'] = 'Total_outfit'
        data.append(total_outfit)
        total_rep['KT_numbering'] += total_outfit['KT_numbering']
    total_rep['name'] = 'ИТОГО за РЕСПУБЛИКУ:'
    total_rep['color'] = 'Total_country'
    data.append(total_rep)
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated,])
def get_report_118(request):
    outfit = request.GET.get("outfit")
    queryset = AmbulanceNumsBase.objects.all().order_by('outfit')
    queryset = ambul_filter(queryset, outfit)
    outfits = ambul_distinct(queryset, 'outfit')

    data = []
    content = DictWithRound({
        'name':None,
        'id': None,
        'code': None,
        'main_num': None,
        'first_redirection': None,
        'second_redirection': None,
        'third_redirection': None,
        'comments': None, 'color': None
    })
    for outfit in outfits.iterator():
        out_data = copy.deepcopy(content)
        out_data['name'] = outfit.outfit.outfit
        out_data['color'] = "outfit"
        data.append(out_data)
        for a in queryset.filter(outfit=outfit.outfit).iterator():
            ambul_data = copy.deepcopy(content)
            ambul_data['id'] = a.id
            ambul_data['name'] = a.region
            ambul_data['code'] = a.code
            ambul_data['main_num'] = a.main_num
            ambul_data['first_redirection'] = a.first_redirection
            ambul_data['second_redirection'] = a.second_redirection
            ambul_data['third_redirection'] = a.third_redirection
            ambul_data['comments'] = a.comments
            data.append(ambul_data)
    return JsonResponse(data, safe=False)

class AmbulBaseUpdateDelete(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = AmbulanceNumsBase.objects.all().order_by('outfit')
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'list':
            return AmbulBaseSerializer
        else:
            return AmbulBaseCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action =='retrieve':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, IsVtorichkaOnly | SuperUser, IngenerUser | SuperUser]
        return [permission() for permission in permission_classes]