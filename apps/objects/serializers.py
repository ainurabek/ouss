from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Object, TPO, Outfit, TypeOfLocation

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


class ObjectListSerializer(serializers.ModelSerializer):
    # trakt=TraktListSerializer(source='trakt_lp', many=True, required=False)
    class Meta:
        model = Object
        fields = '__all__'
        depth = 1

class LPCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        depth = 1