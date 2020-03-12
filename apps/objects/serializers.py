from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Object, TPO, Outfit, TypeOfLocation, Point, IP, TraktOrLine, LineType

User = get_user_model()


class TPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPO
        fields = ('id', 'name', 'index')
        depth = 1

# class OutfitSerializer(serializers.Serializer):
#
#
#     outfit = serializers.CharField(max_length=120)
#     adding = serializers.CharField()
#     num_outfit = serializers.CharField()
#     tpo_id = serializers.IntegerField()
#     type_outfit_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Outfit.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.outfit = validated_data.get('outfit', instance.outfit)
#         instance.adding = validated_data.get('adding', instance.adding)
#         instance.num_outfit = validated_data.get('num_outfit', instance.num_outfit)
#         instance.tpo_id = validated_data.get('tpo_id', instance.tpo_id)
#         instance.type_outfit_id = validated_data.get('type_outfit_id', instance.type_outfit_id)
#         instance.save()
#         return instance



class OutfitSerializer(serializers.ModelSerializer):
    # tpo = TPOSerializer()
    # tpo_id = serializers.RelatedField(source="out_tpo.id", read_only=True)
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    type_outfit = serializers.PrimaryKeyRelatedField(
         read_only=False, queryset=TypeOfLocation.objects.all())
    class Meta:
        model = Outfit
        fields = ('id', 'outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit', 'created_by')
        depth = 1

class PointSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    class Meta:
        model = Point
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo')
        depth = 1

class IPSerializer(serializers.ModelSerializer):
    tpo_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point_id = serializers.PrimaryKeyRelatedField(
         read_only=False, queryset=Point.objects.all())
    # object_id = serializers.PrimaryKeyRelatedField(
    #     read_only=False, queryset=Object.objects.all())
    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1

class LPSerializer(serializers.ModelSerializer):
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
    trakt_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TraktOrLine.objects.all())
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=LineType.objects.all())
    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'trakt_line', 'type_line',
                  'comments', 'created_by', 'created_at')
        depth = 1

