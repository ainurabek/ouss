from rest_framework import serializers

from apps.analysis.models import FormAnalysis, Punkt5, TotalData, Punkt7, Form61KLS, MethodLaying, TypeCable, \
    TypeConnection, TypeEquipment, Form61RRL
from apps.dispatching.models import Event, HistoricalEvent

from apps.dispatching.serializers import EventObjectSerializer, EventCircuitSerializer
from apps.opu.objects.models import Outfit, Point
from apps.opu.objects.serializers import IPListSerializer, PointList, OutfitListSerializer

from apps.analysis.models import AmountChannelsKLSRRL



class DispEvent1ListSerializer(serializers.ModelSerializer):
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    ips = IPListSerializer()
    index1 = serializers.SlugRelatedField(slug_field='index', read_only=True)
    responsible_outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)

    class Meta:
        model = Event
        fields = ('id', "object", "ips", "circuit", "index1", "date_from", "date_to",
                  "point1", 'point2', "comments1", 'reason', 'responsible_outfit')
        depth = 1


class HistoryEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoricalEvent
        fields = ('history_id', "history_date", "history_user", 'history_type',
                  'get_history_type_display')
        depth = 1


class TotalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TotalData
        fields = ("id", "total_length", "total_coefficient", "kls", "vls", "rrl")


class Punkt5Serializer(serializers.ModelSerializer):
    total_data5 = serializers.SlugRelatedField(slug_field="total_coefficient", read_only=True)

    class Meta:
        model = Punkt5
        fields = ("id", "total_data5")


class Punkt7Serializer(serializers.ModelSerializer):
    total_data7 = serializers.SlugRelatedField(slug_field="total_coefficient", read_only=True)

    class Meta:
        model = Punkt5
        fields = ("id", "total_data7")



class Punkt5ListSerializer(serializers.ModelSerializer):
    outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)
    total_data5 = TotalDataSerializer()
    class Meta:
        model = Punkt5
        exclude = ("form_analysis",)


class FormAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormAnalysis
        fields = ("id", "name", "date_from", "date_to")


class FormAnalysisDetailSerializer(serializers.ModelSerializer):
    punkt5 = Punkt5Serializer()
    punkt7 = Punkt7Serializer()
    outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)

    class Meta:
        model = FormAnalysis
        fields = ("id", "outfit", "average_coefficient", "coefficient", "punkt5", "punkt7")


class FormAnalysisUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormAnalysis
        fields = ("id", "name", "average_coefficient")


class Punkt5UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punkt5
        fields = ("id", "outfit_period_of_time_kls", "outfit_period_of_time_rrl", "outfit_period_of_time_vls",
                  "length_kls", "length_vls", "length_rrl",  "formula_activate")


class Punkt7UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punkt7
        fields = ("id", "total_number_kls", "corresponding_norm_kls", "total_number_vls", "corresponding_norm_vls",
                  "total_number_rrl", "corresponding_norm_rrl", )

class Punkt7ListSerializer(serializers.ModelSerializer):
    outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)
    total_data7 = TotalDataSerializer()
    class Meta:
        model = Punkt7
        exclude = ("form_analysis",)


class FormAnalysisCreateSerializer(serializers.ModelSerializer):
    date_from = serializers.DateField(read_only=False, allow_null=False)
    date_to = serializers.DateField(read_only=False, allow_null=False)

    class Meta:
        model = FormAnalysis
        fields = ("id", "date_from", "date_to")


class AmountChannelsKLSRRLSerializer(serializers.ModelSerializer):

    class Meta:
        model = AmountChannelsKLSRRL
        fields = ("id", "amount_channelsKLS", "amount_channelsRRL")

class MethodLayingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodLaying
        fields = ("id", "name")

class TypeCableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCable
        fields = ('id', 'name',)

class TypeConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeConnection
        fields = ("id", "name")

class TypeEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEquipment
        fields = ("id", "name")

class Form61KLSCreateSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    laying_method = serializers.PrimaryKeyRelatedField(queryset=MethodLaying.objects.all(), many=True)
    type_cable = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=TypeCable.objects.all())
    type_connection = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeConnection.objects.all())

    class Meta:
        model = Form61KLS
        fields = ('outfit', 'point1', 'point2', 'total_length_line', 'total_length_cable', 'above_ground',
                  'under_ground', 'year_of_laying', 'laying_method', 'type_cable', 'type_connection', 'src')
        depth = 1


class Form61KLSSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    outfit = OutfitListSerializer()
    laying_method = MethodLayingSerializer(many=True, read_only=True)
    type_connection = TypeConnectionSerializer()
    type_cable = TypeCableSerializer()

    class Meta:
        model = Form61KLS
        fields = ("__all__")


class Form61KLSEditSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    laying_method = serializers.PrimaryKeyRelatedField(queryset=MethodLaying.objects.all(), many=True)
    type_cable = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=TypeCable.objects.all())
    type_connection = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeConnection.objects.all())

    class Meta:
        model = Form61KLS
        fields = ('outfit', 'total_length_line', 'total_length_cable', 'above_ground',
                  'under_ground', 'year_of_laying', 'laying_method', 'type_cable', 'type_connection')
        depth = 1

class Form61RRLCreateSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    type_equipment_rrl = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=TypeEquipment.objects.all())
    type_connection = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeConnection.objects.all())

    class Meta:
        model = Form61RRL
        fields = ('outfit', 'point1', 'point2', 'total_length_line', 'type_equipment_rrl', 'type_connection')
        depth = 1

class Form61RRLSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    outfit = OutfitListSerializer()
    type_connection = TypeConnectionSerializer()
    type_equipment_rrl = TypeEquipmentSerializer()

    class Meta:
        model = Form61RRL
        fields = ("__all__")

class Form61RRLEditSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    type_equipment_rrl = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeEquipment.objects.all())
    type_connection = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeConnection.objects.all())

    class Meta:
        model = Form61RRL
        fields = ('outfit', 'total_length_line', 'type_equipment_rrl', 'type_connection')
        depth = 1