from rest_framework import serializers
from apps.opu.customer.models import Customer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object, Point
from apps.opu.circuits.serializers import CategorySerializer
from apps.opu.objects.serializers import ConsumerSerializer, BridgeListSerializer, OrderObjectPhotoSerializer


class CustomerForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "customer", 'abr')


class PointForm51Serializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("name", "point")


class Form51CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.1"""
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())

    class Meta:
        model = Form51
        fields = ("id", "customer", "comments")


class ObjectForm51Serializer(serializers.ModelSerializer):
    bridges = BridgeListSerializer(many=True)
    category = CategorySerializer()
    consumer = ConsumerSerializer()
    order_object_photo = OrderObjectPhotoSerializer(many=True)

    class Meta:
        model = Object
        fields = ("name", "category", "bridges", "consumer", "comments", "order_object_photo")
        depth = 1


class Form51Serializer(serializers.ModelSerializer):
    """Список Формы 5.1"""
    object = ObjectForm51Serializer()
    customer = CustomerForm51Serializer()

    class Meta:
        model = Form51
        fields = ("id", "object", "customer", "comments")
        depth = 1
