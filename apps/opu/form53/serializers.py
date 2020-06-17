from rest_framework import serializers

from apps.dispatching.models import Region
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer

from apps.opu.form53.models import Form53

from apps.opu.circuits.models import Circuit

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