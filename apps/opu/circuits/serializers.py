from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Circuit
from ..customer.models import Customer
from ..objects.models import Category, Object, Point

User = get_user_model()


class ObjectCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class PointCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('id', 'name', 'point')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'index', 'name')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TransitCircSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Circuit
        fields = ('id', 'point1', 'name', 'point2')


class CircuitList(serializers.ModelSerializer):
    id_object = ObjectCircSerializer(many=True)
    point1 = PointCircSerializer()
    point2 = PointCircSerializer()
    transit = TransitCircSerializer(many=True)
    transit2 = TransitCircSerializer(many=True)
    customer = CustomerSerializer()
    category = CategorySerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'id_object', 'num_circuit', 'category', 'num_order',
                   'comments', 'transit', 'transit2', 'first', 'point1', 'point2',
                  'customer')

class CircuitTrassaList(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ('id', 'num_circuit')

class CircuitEdit(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Category.objects.all())

    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())


    class Meta:
        model = Circuit
        fields = ('category', 'num_order', 'comments', 'first', 'point1', 'point2',
                  'customer')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """

        instance.num_order = validated_data.get('num_order', instance.num_order)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.category = validated_data.get('category', instance.category)
        instance.point1 = validated_data.get('point1', instance.point1)
        instance.point2 = validated_data.get('point2', instance.point2)
        instance.first = validated_data.get('first', instance.first)
        instance.save()
        return instance


class CircuitDetail(serializers.ModelSerializer):
    transit = TransitCircSerializer(many=True)
    transit2 = TransitCircSerializer(many=True)

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'transit', 'transit2')
