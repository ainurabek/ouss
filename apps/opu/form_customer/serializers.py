from rest_framework import serializers

from apps.opu.form_customer.models import Form_Customer, Signalization, OrderCusPhoto
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer
from apps.opu.circuits.models import Circuit

from apps.opu.customer.models import Customer

from apps.opu.objects.serializers import BridgeListSerializer

from apps.opu.circuits.serializers import TransitCircSerializer

from apps.opu.circuits.serializers import CircuitTrassaerializer


class CustomerFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'abr', 'customer')


class OrderCusPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCusPhoto
        fields = ("id", "src")


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('id', "point", "name")


class CircuitTransitSerializer(serializers.ModelSerializer):
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Circuit
        fields = ('id', "point1", "name", "point2")


class CircuitListSerializer(serializers.ModelSerializer):

    point1 = PointSerializer()
    point2 = PointSerializer()
    trassa = CircuitTrassaerializer()

    class Meta:
        model = Circuit
        fields = ('id', "name", "point1", "point2", 'trassa')


class CircuitSerializer(serializers.ModelSerializer):
    trassa = CircuitTrassaerializer()

    class Meta:
        model = Circuit
        fields = ('trassa',)


class ObjectFormCustomer(serializers.ModelSerializer):
    bridges = BridgeListSerializer(many=True)

    class Meta:
        model = Object
        fields = ('bridges', 'name')


class SignalizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signalization
        fields = ("id", "name")


class FormCustomerSerializer(serializers.ModelSerializer):
    object = ObjectFormCustomer()
    circuit = CircuitSerializer()
    signalization = SignalizationSerializer()
    customer = CustomerFormSerializer()
    order_cust_photo = OrderCusPhotoSerializer(many=True)
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Form_Customer
        fields = ("id", "circuit", 'customer', "object", "amount_flow", "signalization",
                  "type_of_using", "num_order", "order_cust_photo", "comments", 'point1', 'point2')


class FormCustomerCreateSerializer(serializers.ModelSerializer):
    """Создания Формы арендаторов"""
    signalization = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Signalization.objects.all())

    class Meta:
        model = Form_Customer
        fields = ('id', "amount_flow", "signalization", "type_of_using", "num_order", "comments")
