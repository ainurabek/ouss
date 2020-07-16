from rest_framework import serializers
from apps.opu.form51.models import Region
from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo
from apps.opu.circuits.serializers import CircuitList


class Order53PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order53Photo
        fields = ("id", "order")

class Schema53PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema53Photo
        fields = ("id", "schema")

class Form53CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.3"""

    class Meta:
        model = Form53
        fields = ("id",  "order", "schema", "comments")

class Form53Serializer(serializers.ModelSerializer):
    """Список Формы 5.3"""
    order = Order53PhotoSerializer()
    schema=Schema53PhotoSerializer()
    circuit = CircuitList()
    class Meta:
        model = Form53
        fields = ("id", "circuit",  "order", "schema", "comments", 'created_at')
        depth=1

class Region53Serializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("id", "name", "slug",)