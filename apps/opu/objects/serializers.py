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


class OutfitListSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    type_outfit = TypeOfLocationSerializer()

    class Meta:
        model = Outfit
        fields = ('id', 'outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit', 'created_by')
        depth = 1


class OutfitCreateSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    type_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeOfLocation.objects.all())

    class Meta:
        model = Outfit
        fields = ('id', 'outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit', 'created_by')
        depth = 1


class PointListSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    id_outfit = OutfitListSerializer()
    class Meta:
        model = Point
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo')
        depth = 1


class PointCreateSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())

    class Meta:
        model = Point
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo')
        depth = 1


class IPListSerializer(serializers.ModelSerializer):
    tpo_id = TPOSerializer()
    point_id = PointListSerializer()

    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1


class IPCreateSerializer(serializers.ModelSerializer):
    tpo_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    object_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Object.objects.all())

    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1


class ParentSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2')


class TransitSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Object
        fields = ('point1', 'name', 'point2')


class LPSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_line = serializers.SlugRelatedField(slug_field='name', read_only=True)
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'trakt', 'type_line', 'transit', 'transit2')
        depth = 1


class LPCreateSerializer(serializers.ModelSerializer):
    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=LineType.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'trakt', 'type_line', 'our',
                  'comments', 'created_by', 'created_at')
        depth = 1


class ObjectSerializer(serializers.ModelSerializer):
    id_parent=ParentSerializer()
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_of_trakt = TypeOfTraktSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'id_parent', 'name', 'trakt', 'point1', 'point2', 'type_of_trakt', 'transit', 'transit2')

class ObjectCreateSerializer(serializers.ModelSerializer):
    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
         read_only=False, queryset=Point.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
         read_only=False, queryset=Point.objects.all())
    type_of_trakt = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeOfTrakt.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'id_parent','name', 'id_outfit', 'trakt', 'tpo1', 'point1', 'tpo2', 'point2', 'type_of_trakt', 'system', 'amount_channels', 'type_line', 'our', 'num', 'transit', 'transit2')


class SelectObjectSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt', 'transit', 'transit2')


class ObjectListSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_of_trakt = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt')


class PointList(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('id', 'point')


class ObjectFilterSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Object
        fields = ('name', 'point1', 'point2', 'COreceive', 'COdeliver', 'id_outfit')