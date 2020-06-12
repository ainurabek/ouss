from rest_framework import serializers

from apps.dispatching.models import Region
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer

from apps.opu.form53.models import Form53

from apps.opu.circuits.models import Circuit


class PointForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("name", "point")


class Form53CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.3"""

    class Meta:
        model = Form53
        fields = ("id",  "order", "schema")


class CircuitForm53Serializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointForm51Serializer()
    point2 = PointForm51Serializer()

    class Meta:
        model = Circuit
        fields = ('num_circuit', 'final_destination', 'name', 'type_using', 'category', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                  'type_transit1', 'type_transit2', 'transit', 'transit2', 'in_out', 'first', 'point1',
                  'point2', 'customer', 'mode', 'type_com', 'id_object')


class Form53Serializer(serializers.ModelSerializer):
    """Список Формы 5.3"""
    circuit = CircuitForm53Serializer()


    class Meta:
        model = Form53
        fields = ("id", "circuit",  "order", "schema")
        depth=1

class Region53Serializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("id", "name", "slug",)