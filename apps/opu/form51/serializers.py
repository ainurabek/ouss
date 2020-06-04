from rest_framework import serializers

from apps.dispatching.models import Region
from apps.opu.customer.models import Customer
from apps.opu.form51.models import Form51
from apps.opu.objects.models import Object


class Form51CreateSerializer(serializers.ModelSerializer):
    """Создания Формы 5.1"""
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Customer.objects.all())
    # reserve_object = serializers.ManyRelatedField()

    class Meta:
        model = Form51
        exclude = ("object",)


class Form51Serializer(serializers.ModelSerializer):
    """Список Формы 5.1"""
    class Meta:
        model = Form51
        exclude = ("object_reserve", )
        depth=1


class RegionSerializer(serializers.ModelSerializer):
    """ Регионы """

    class Meta:
        model = Region
        fields = ("__all__",)


class ObjectReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = ("name", "transit", "transit2", "category")


class Form51ReserveSerializer(serializers.ModelSerializer):
    """ Резерв """
    object_reserve = ObjectReserveSerializer()

    class Meta:
        model = Form51
        fields = ("object_reserve",)
        depth = 1