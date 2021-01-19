from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Circuit, TypeCom, Mode, Speed, Measure
from ..customer.models import Customer
from ..objects.models import Category, Object, Point

User = get_user_model()


class SpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speed
        fields = '__all__'


class ObjectCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class PointCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('id', 'name', 'point')


class TypeComSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCom
        fields = ('id', 'name')


class MeasureCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ('id', 'name')

class ModeCircSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode
        fields = ('id', 'name')


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
    type_com = TypeComSerializer()
    customer = CustomerSerializer()
    mode = ModeCircSerializer()
    measure = MeasureCircSerializer()
    category = CategorySerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'id_object', 'num_circuit', 'type_using', 'category', 'num_order',
                   'speed', 'measure', 'comments', 'transit', 'transit2', 'first', 'point1', 'point2',
                  'customer', 'mode', 'type_com')


class CircuitEdit(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Category.objects.all())
    measure = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Measure.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())
    mode = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Mode.objects.all())
    type_com = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeCom.objects.all())

    class Meta:
        model = Circuit
        fields = ('type_using', 'category', 'num_order',
                  'date_order', 'speed', 'measure', 'comments', 'first', 'point1', 'point2',
                  'customer', 'mode', 'type_com')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.type_using = validated_data.get('type_using', instance.type_using)
        instance.num_order = validated_data.get('num_order', instance.num_order)
        instance.date_order = validated_data.get('date_order', instance.date_order)
        instance.speed = validated_data.get('speed', instance.speed)
        instance.measure = validated_data.get('measure', instance.measure)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.mode = validated_data.get('mode', instance.mode)
        instance.type_com = validated_data.get('type_com', instance.type_com)
        instance.category = validated_data.get('category', instance.category)
        instance.point1 = validated_data.get('point1', instance.point1)
        instance.point2 = validated_data.get('point2', instance.point2)
        instance.first = validated_data.get('first', instance.first)
        instance.save()
        return instance
