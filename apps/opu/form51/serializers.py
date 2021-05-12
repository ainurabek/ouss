from rest_framework import serializers
from apps.opu.customer.models import Customer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.circuits.serializers import CategorySerializer
from apps.opu.form51.models import OrderPhoto, SchemaPhoto
from apps.opu.objects.serializers import ConsumerSerializer
from apps.opu.objects.serializers import BridgeListSerializer


class CustomerForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "customer", 'abr')


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

    class Meta:
        model = Form51
        fields = ("id", "customer", "num_order", "reserve", "comments")


class ObjectForm51Serializer(serializers.ModelSerializer):
    bridges = BridgeListSerializer(many=True)
    category = CategorySerializer()
    consumer = ConsumerSerializer()

    class Meta:
        model = Object
        fields = ("name", "category", 'bridges', 'consumer')
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
    category = CategorySerializer()

    class Meta:
        model = Object
        fields = ('id', "name", "reserve_transit", "reserve_transit2", "category")


class Form51ReserveSerializer(serializers.ModelSerializer):
    """ Резерв """
    object = ObjectReserveSerializer()

    class Meta:
        model = Form51
        fields = ("id", "object")
        depth = 1