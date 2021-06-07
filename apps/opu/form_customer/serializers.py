from rest_framework import serializers

from apps.opu.form_customer.models import Form_Customer, Signalization, OrderCusPhoto
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import TransitSerializer
from apps.opu.circuits.models import Circuit

from apps.opu.customer.models import Customer

from apps.opu.objects.serializers import BridgeListSerializer

from apps.opu.circuits.serializers import TransitCircSerializer

from apps.opu.circuits.serializers import CircuitTrassaerializer

from apps.opu.objects.serializers import TPOSerializer, PointList, OutfitListSerializer, CategorySerializer


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
    customer = CustomerFormSerializer()

    class Meta:
        model = Circuit
        fields = ( 'id', 'trassa', 'customer')


class ObjectFormCustomer(serializers.ModelSerializer):
    bridges = BridgeListSerializer(many=True)
    point1 = PointSerializer()
    point2 = PointSerializer()
    customer = CustomerFormSerializer()

    class Meta:
        model = Object
        fields = ('id', 'bridges', 'customer', 'name', 'point1', 'point2')


class SignalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signalization
        fields = ("id", "name")


class FormCustomerSerializer(serializers.ModelSerializer):
    object = ObjectFormCustomer()
    circuit = CircuitSerializer()
    signalization = SignalizationSerializer()
    order_cust_photo = OrderCusPhotoSerializer(many=True)
    point1 = PointSerializer()
    point2 = PointSerializer()
    class Meta:
        model = Form_Customer
        fields = ("id", "circuit", "object", "amount_flow", "signalization",
                  "type_of_using", "num_order", "order_cust_photo", "comments", 'point1', 'point2')


class FormCustomerCreateSerializer(serializers.ModelSerializer):
    """Создания Формы арендаторов"""
    signalization = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Signalization.objects.all())

    class Meta:
        model = Form_Customer
        fields = ('id', "amount_flow", "signalization", "type_of_using", "num_order", "comments")


class AllObjectFormSerializer(serializers.ModelSerializer):
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointList()
    point2 = PointList()
    bridges = BridgeListSerializer(many=True)
    id_outfit = OutfitListSerializer()
    category = CategorySerializer()
    customer = CustomerFormSerializer()


    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'category', 'point1', 'point2', 'tpo1', 'tpo2', 'customer', 'bridges')
        depth = 1

class CircuitFormList(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    trassa = CircuitTrassaerializer()
    customer = CustomerFormSerializer()
    category = CategorySerializer()

    # object = ObjectSerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'num_circuit', 'category', 'num_order', 'comments', 'trassa', 'first',
                  'point1', 'point2', 'customer', 'object')


class EventObjFormCustSerializer(serializers.ModelSerializer):
    form_customer= FormCustomerSerializer()
    bridges = BridgeListSerializer(many=True)
    customer = serializers.SlugRelatedField(slug_field="customer", read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'customer', 'form_customer', 'bridges')
        depth = 1

class EventCircuitFormCustSerializer(serializers.ModelSerializer):
    form_customer= FormCustomerSerializer()
    trassa = TransitCircSerializer(many=True)
    customer = serializers.SlugRelatedField(slug_field="customer", read_only=True)

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'customer',  'form_customer', 'trassa')
        depth = 1
