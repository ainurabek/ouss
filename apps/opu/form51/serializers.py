from rest_framework import serializers

from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer

from apps.opu.circuits.serializers import CategorySerializer

from apps.opu.form51.models import OrderPhoto, SchemaPhoto

from apps.opu.objects.serializers import ConsumerSerializer


class CustomerForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "customer", 'abr' )

class PointForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("name", "point")


class OrderPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPhoto
        fields = ("id", "src")

class SchemaPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaPhoto
        fields = ("id", "src")

class Form51CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.1"""
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())
    reserve_object = serializers.PrimaryKeyRelatedField(
        read_only=False, many=True, allow_null=True,  queryset=Object.objects.all())

    class Meta:
        model = Form51
        fields = ("id", "customer", "num_order", "reserve", "comments")




class ObjectForm51Serializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointForm51Serializer()
    point2 = PointForm51Serializer()
    category = CategorySerializer()
    consumer = ConsumerSerializer()

    class Meta:
        model = Object
        fields = ("name", "transit", "transit2", "category", "point1", "point2", 'consumer')
        depth = 1


class Form51Serializer(serializers.ModelSerializer):
    """Список Формы 5.1"""
    object = ObjectForm51Serializer()
    customer = CustomerForm51Serializer()
    order_photo = OrderPhotoSerializer(many=True)
    schema_photo = SchemaPhotoSerializer(many=True)

    class Meta:
        model = Form51
        fields = ("id", "object", "customer", "num_order", "order_photo", "schema_photo", "reserve", 'comments')
        depth=1




class ObjectReserveSerializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Object
        fields = ('id', "name", "reserve_transit", "reserve_transit2", "category")


class Form51ReserveSerializer(serializers.ModelSerializer):
    """ Резерв """
    object = ObjectReserveSerializer(many=True)

    class Meta:
        model = Form51
        fields = ("id", "object")
        depth = 1