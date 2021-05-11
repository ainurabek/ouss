from rest_framework import serializers

from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo


from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import PointCircSerializer
from apps.opu.objects.serializers import CategorySerializer

from apps.opu.circuits.serializers import TransitCircSerializer


class Order53PhotoSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField('get_src_url')
    class Meta:
        model = Order53Photo
        fields = ("id", "src")
    def get_src_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.src.url)


class Schema53PhotoSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField('get_src_url')

    class Meta:
        model = Schema53Photo
        fields = ("id", "src")
    def get_src_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.src.url)


class Form53CreateSerializer(serializers.ModelSerializer):

    """Создания Формы 5.3"""

    class Meta:
        model = Form53
        fields = ("id",  "comments")


# class TransitForm53Serializer(serializers.ModelSerializer):
#     point1 = PointCircSerializer()
#     point2 = PointCircSerializer()
#
#     class Meta:
#         model = Circuit
#         fields = ('id', 'point1', 'name', 'point2')


class CircuitForm53(serializers.ModelSerializer):

    trassa = TransitCircSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name',  'num_circuit', 'category', 'num_order',
                   'comments', 'trassa',)


class Form53Serializer(serializers.ModelSerializer):
    """Список Формы 5.3"""
    order53_photo = Order53PhotoSerializer(many=True)
    schema53_photo = Schema53PhotoSerializer(many=True)
    circuit = CircuitForm53()

    class Meta:
        model = Form53
        fields = ("id", "circuit",  "order53_photo", "schema53_photo", "comments")
        depth = 1

