from rest_framework import serializers

from apps.opu.form51.models import Region
from apps.opu.form_customer.models import Form_Customer, Signalization, OrderCusPhoto
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer
from apps.opu.circuits.models import Circuit

from apps.opu.customer.models import Customer


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
        fields = ("point", "name")


class CircuitTransitSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Circuit
        fields = ('id', "point1", "name", "point2")


class CircuitListSerializer(serializers.ModelSerializer):

    point1 = PointSerializer()
    point2 = PointSerializer()
    transit = CircuitTransitSerializer(many=True)
    transit2 = CircuitTransitSerializer(many=True)

    class Meta:
        model = Circuit
        fields = ('id', "name", "point1", "point2", "transit", "transit2")


class CircuitSerializer(serializers.ModelSerializer):
    transit = CircuitTransitSerializer(many=True)
    transit2 = CircuitTransitSerializer(many=True)
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Circuit
        fields = ("name", "transit", "transit2", "point1", "point2")


class ObjectFormCustomer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointSerializer()
    point2 = PointSerializer()

    class Meta:
        model = Object
        fields = ( 'id', "name", "transit", "transit2", "point1", "point2")


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

    class Meta:
        model = Form_Customer
        fields = ("id", "circuit", 'customer', "object", "amount_flow", "signalization",
                  "type_of_using", "num_order", "order_cust_photo", "comments")


class FormCustomerCreateSerializer(serializers.ModelSerializer):
    """Создания Формы арендаторов"""
    signalization = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Signalization.objects.all())

    class Meta:
        model = Form_Customer
        fields = ('id', "amount_flow", "signalization", "type_of_using", "num_order", "comments")
