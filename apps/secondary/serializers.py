from rest_framework import serializers

from apps.secondary.models import TypeStation


class TypeStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeStation
        fields = ('id', "name")