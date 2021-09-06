from rest_framework import serializers
from apps.secondary.models import TypeStation
from apps.opu.objects.serializers import OutfitListSerializer, PointList, PointListSerializer
from apps.secondary.models import SecondaryBase, AmbulanceNumsBase

from apps.opu.objects.models import Outfit, Point


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
                  'active_value', 'active_numbering', 'free_numbering', 'GAS_numbering', 'zone_code', 'inner_zone_code', 'amount_of_numbers'
                  'KT_numbering', 'comments', 'administrative_division')
        depth = 1

class SecondaryBaseCreateSerializer(serializers.ModelSerializer):
    point = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    type_station = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeStation.objects.all())


    class Meta:
        model = SecondaryBase
        fields = ('id', 'point', 'outfit', 'type_station', 'year_of_launch', 'installed_value',
                  'active_value', 'active_numbering', 'free_numbering', 'GAS_numbering', 'KT_numbering', 'comments', 'administrative_division')
        depth = 1

class AmbulBaseSerializer(serializers.ModelSerializer):
    outfit = OutfitListSerializer()

    class Meta:
        model = AmbulanceNumsBase
        fields = ('id', 'outfit', 'region', 'code', 'main_num', 'first_redirection',
                  'second_redirection', 'third_redirection', 'comments')
        depth = 1

class AmbulBaseCreateSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())

    class Meta:
        model = AmbulanceNumsBase
        fields = ('id', 'outfit', 'region', 'code', 'main_num', 'first_redirection',
                  'second_redirection', 'third_redirection', 'comments')
        depth = 1