from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Circuit, TypeCom, Mode, Speed, Measure
from ..customer.models import Customer
from ..objects.models import Category, Object, Point, InOut

User = get_user_model()


class ObjectCircSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = ('__all__')


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

class InOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = InOut
        fields = ('id', 'name')

class ModeCircSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mode
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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
    id_object = ObjectCircSerializer()
    point1=PointCircSerializer()
    point2=PointCircSerializer()
    transit = TransitCircSerializer(many=True)
    transit2 = TransitCircSerializer(many=True)
    type_com = TypeComSerializer()
    customer = CustomerSerializer()
    mode = ModeCircSerializer()
    in_out=InOutSerializer()
    measure = MeasureCircSerializer()
    category = CategorySerializer()
    class Meta:
        model = Circuit
        fields = ('id', 'name', 'number', 'id_object', 'num_circuit', 'type_using', 'category', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                   'transit', 'transit2', 'in_out', 'first', 'point1', 'point2',
                  'customer', 'mode', 'type_com')

class CircuitEdit(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Category.objects.all())
    measure = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=Measure.objects.all())
    in_out = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=InOut.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())
    mode = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=Mode.objects.all())
    type_com = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeCom.objects.all())
    class Meta:
        model = Circuit
        fields = ('number', 'type_using', 'category', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                   'in_out', 'first', 'point1', 'point2',
                  'customer', 'mode', 'type_com')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.number = validated_data.get('number', instance.number)
        instance.type_using = validated_data.get('type_using', instance.type_using)
        instance.num_order = validated_data.get('num_order', instance.num_order)
        instance.date_order = validated_data.get('date_order', instance.date_order)
        instance.num_arenda = validated_data.get('num_arenda', instance.num_arenda)
        instance.speed = validated_data.get('speed', instance.speed)
        instance.measure = validated_data.get('measure', instance.measure)
        instance.adding = validated_data.get('adding', instance.adding)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.in_out = validated_data.get('in_out', instance.in_out)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.mode = validated_data.get('mode', instance.mode)
        instance.type_com = validated_data.get('type_com', instance.type_com)
        instance.category = validated_data.get('category', instance.category)
        instance.point1 = validated_data.get('point1', instance.point1)
        instance.point2 = validated_data.get('point2', instance.point2)
        instance.save()
        return instance

