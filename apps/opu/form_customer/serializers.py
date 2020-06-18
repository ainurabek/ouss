from rest_framework import serializers

from apps.dispatching.models import Region
from apps.opu.form_customer.models import Form_Customer, Signalization
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer
from apps.opu.circuits.models import Circuit


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("point", "name")


class CircuitTransitSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Circuit
        fields = ("point1", "name", "point2")


class CircuitListSerializer(serializers.ModelSerializer):
    object = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point1 = PointSerializer()
    point2 = PointSerializer()
    transit = CircuitTransitSerializer(many=True)
    transit2 = CircuitTransitSerializer(many=True)

    class Meta:
        model = Circuit
        fields = ("object", "name", "point1", "point2", "transit", "transit2")


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
        fields = ("name", "transit", "transit2", "point1", "point2")


class SignalizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signalization
        fields = ("id", "name")


class FormCustomerSerializer(serializers.ModelSerializer):
    object = ObjectFormCustomer()
    circuit = CircuitSerializer()
    signalization = SignalizationSerializer()

    class Meta:
        model = Form_Customer
        fields = ("id", "circuit", "object", "amount_flow", "signalization", "type_of_using", "num_order", "order", "comments")


class FormCustomerCreateSerializer(serializers.ModelSerializer):
    """Создания Формы арендаторов"""
    signalization = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Signalization.objects.all())

    class Meta:
        model = Form_Customer
        fields = ("amount_flow", "signalization", "type_of_using", "num_order", "order", "comments")
