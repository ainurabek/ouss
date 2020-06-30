from rest_framework import serializers

from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.form51.models import Form51, Region
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer

from apps.opu.circuits.serializers import CategorySerializer

from apps.opu.form51.models import Image


class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ('id', 'image', 'name', 'created_at')

class CustomerForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "customer", 'abr' )

class PointForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("name", "point")


class Form51CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.1"""
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())
    reserve_object = serializers.PrimaryKeyRelatedField(
        read_only=False, many=True,  queryset=Object.objects.all())


    class Meta:
        model = Form51
        fields = ("id", "customer", "num_ouss", "order", "schema", "reserve", "report_num", "reserve_object")


class ObjectForm51Serializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointForm51Serializer()
    point2 = PointForm51Serializer()
    category = CategorySerializer()

    class Meta:
        model = Object
        fields = ("name", "transit", "transit2", "category", "point1", "point2")
        depth = 1


class Form51Serializer(serializers.ModelSerializer):
    """Список Формы 5.1"""
    object = ObjectForm51Serializer()
    customer = CustomerForm51Serializer()


    class Meta:
        model = Form51
        fields = ("id", "object", "customer", "num_ouss", "order", "schema", "reserve", "report_num", "reserve_object")
        depth=1


class RegionSerializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("id", "name", "slug", )


class ObjectReserveSerializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Object
        fields = ('id', "name", "transit", "transit2", "category")


class Form51ReserveSerializer(serializers.ModelSerializer):
    """ Резерв """
    reserve_object = ObjectReserveSerializer(many=True)

    class Meta:
        model = Form51
        fields = ("id", "reserve_object")
        depth = 1