from rest_framework import serializers
from apps.secondary.models import TypeStation
from apps.opu.objects.serializers import OutfitListSerializer, PointList, PointListSerializer
from apps.secondary.models import SecondaryBase


class TypeStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeStation
        fields = ('id', "name")

class SecondaryBaseSerializer(serializers.ModelSerializer):
    point = PointListSerializer()
    outfit = OutfitListSerializer()
    type_station = TypeStationSerializer()


    class Meta:
        model = SecondaryBase
        fields = ('id', 'point', 'outfit', 'type_station', 'year_of_launch', 'installed_value',
                  'active_value', 'active_numbering', 'free_numbering', 'GAS_numbering', 'GAS_return', 'KT_numbering', 'comments')
        depth = 1