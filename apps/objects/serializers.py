from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Object, TPO, Outfit, TypeOfLocation, Point, IP, LineType, TypeOfTrakt

User = get_user_model()


class TPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPO
        fields = ('id', 'name', 'index')
        depth = 1


class TypeOfLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfLocation
        fields = ('name',)


class TypeOfTraktSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfTrakt
        fields = ('name',)


class TypeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineType
        fields = ('name',)


class OutfitSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    type_outfit = TypeOfLocationSerializer()

    class Meta:
        model = Outfit
        fields = ('id', 'outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit', 'created_by')
        depth = 1


class PointSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    id_outfit = OutfitSerializer()
    class Meta:
        model = Point
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo')
        depth = 1


class IPSerializer(serializers.ModelSerializer):
    tpo_id = TPOSerializer()
    point_id = PointSerializer()

    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1



class ParentSerializer(serializers.ModelSerializer):
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2')


class TransitSerializer(serializers.ModelSerializer):
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Object
        fields = ('point1', 'name', 'point2')



class LPSerializer(serializers.ModelSerializer):
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointSerializer()
    point2 = PointSerializer()
    id_outfit = OutfitSerializer()
    type_line = TypeLineSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'trakt', 'type_line', 'our',
                  'comments', 'created_by', 'created_at', 'transit', 'transit2')
        depth = 1



class ObjectSerializer(serializers.ModelSerializer):
    id_parent=ParentSerializer()
    tpo1 = TPOSerializer()
    point1 = PointSerializer()
    tpo2 = TPOSerializer()
    point2 = PointSerializer()
    type_of_trakt = TypeOfTraktSerializer()
    id_outfit = OutfitSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'id_parent','name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'type_of_trakt', 'system', 'amount_channels', 'type_line', 'our', 'num', 'transit', 'transit2')


