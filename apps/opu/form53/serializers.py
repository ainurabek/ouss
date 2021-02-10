from rest_framework import serializers

from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo
from apps.opu.circuits.serializers import CircuitList


class Order53PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order53Photo
        fields = ("id", "src")

class Schema53PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema53Photo
        fields = ("id", "src")

class Form53CreateSerializer(serializers.ModelSerializer):

    """Создания Формы 5.3"""

    class Meta:
        model = Form53
        fields = ("id",  "comments")

class Form53Serializer(serializers.ModelSerializer):
    """Список Формы 5.3"""
    order53_photo = Order53PhotoSerializer(many=True)
    schema53_photo=Schema53PhotoSerializer(many=True)
    circuit = CircuitList()
    class Meta:
        model = Form53
        fields = ("id", "circuit",  "order53_photo", "schema53_photo", "comments")
        depth=1

