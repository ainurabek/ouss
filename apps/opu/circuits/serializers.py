from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Circuit
from ..objects.models import Category

User = get_user_model()


class CircuitList(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ('id', 'name', 'number', 'id_object', 'num_circuit', 'final_destination', 'type_using', 'category', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                  'type_transit1', 'type_transit2', 'transit', 'transit2', 'in_out', 'first', 'point1', 'point2',
                  'id_object', 'customer', 'mode', 'type_com')



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CircuitEdit(serializers.ModelSerializer):


    class Meta:
        model = Circuit
        fields = ('num_circuit', 'final_destination', 'type_using', 'category', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                  'type_transit1', 'type_transit2', 'transit', 'transit2', 'in_out', 'first', 'point1',
                  'point2', 'customer', 'mode', 'type_com')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.category = validated_data.get('category', instance.category)
        instance.point1 = validated_data.get('point1', instance.point1)
        instance.point2 = validated_data.get('point2', instance.point2)
        instance.save()
        return instance

