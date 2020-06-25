from rest_framework import serializers
from apps.opu.form51.models import Region
from apps.opu.form53.models import Form53
from apps.opu.circuits.serializers import CircuitList

class Form53CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.3"""

    class Meta:
        model = Form53
        fields = ("id",  "order", "schema", "comments")

class Form53Serializer(serializers.ModelSerializer):
    """Список Формы 5.3"""
    circuit = CircuitList()
    class Meta:
        model = Form53
        fields = ("id", "circuit",  "order", "schema", "comments")
        depth=1

class Region53Serializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("id", "name", "slug",)