from rest_framework import serializers

from apps.dispatching.models import Region
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer


class PointForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("name", "point")


class Form51CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.1"""
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Customer.objects.all())
    reserve_object = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Object.objects.all(), many=True)

    class Meta:
        model = Form51
        fields = ("id", "customer", "num_ouss", "order", "schema", "reserve", "report_num", "reserve_object")


class ObjectForm51Serializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointForm51Serializer()
    point2 = PointForm51Serializer()

    class Meta:
        model = Object
        fields = ("name", "transit", "transit2", "category", "point1", "point2")
        depth = 1


class Form51Serializer(serializers.ModelSerializer):
    """Список Формы 5.1"""
    object = ObjectForm51Serializer()
    customer = serializers.SlugRelatedField(slug_field="customer", read_only=True)

    class Meta:
        model = Form51
        fields = ("id", "object", "customer", "num_ouss", "order", "schema", "reserve", "report_num")
        depth=1


class RegionSerializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("id", "name", "slug", )


class ObjectReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = ("name", "transit", "transit2", "category")


class Form51ReserveSerializer(serializers.ModelSerializer):
    """ Резерв """
    object_reserve = ObjectReserveSerializer()

    class Meta:
        model = Form51
        fields = ("id", "object_reserve",)
        depth = 1