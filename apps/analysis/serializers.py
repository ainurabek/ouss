from rest_framework import serializers

from apps.analysis.models import FormAnalysis, Item5, SpecificGravityOfLength, SpecificGravityOfLengthTypeLine, \
    OutfitItem5, Item7
from apps.dispatching.models import Event, HistoricalEvent

from apps.dispatching.serializers import EventObjectSerializer, EventCircuitSerializer
from apps.opu.objects.models import MainLineType
from apps.opu.objects.serializers import IPListSerializer


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
        fields = ('id', 'history_id', "history_date", "history_change_reason",
                  "history_user", 'history_type')
        depth = 1


class SpecificGravityOfLengthTypeLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificGravityOfLengthTypeLine
        fields = ("id", "type_line", "value")


class SpecificGravityOfLengthSerializer(serializers.ModelSerializer):
    space = SpecificGravityOfLengthTypeLineSerializer(many=True)

    class Meta:
        model = SpecificGravityOfLength
        fields = ("id", "total_length", "coefficient", "space")


class Item5Serializer(serializers.ModelSerializer):
    type_line = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item5
        fields = ("id", "outfit_period_of_time", "length", "downtime", "coefficient", "type_line")


class OutfitItemSerializer(serializers.ModelSerializer):
    id_parent = serializers.SlugRelatedField(slug_field="id", read_only=True)
    outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)
    total_coefficient = serializers.SlugRelatedField(slug_field="coefficient", read_only=True)

    class Meta:
        model = OutfitItem5
        fields = ("id", "id_parent", "outfit", "total_coefficient")


class Item7Serializer(serializers.ModelSerializer):
    type_line = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Item7
        fields = ("id", "total_object", "corresponding_norm", "type_line", "match_percentage", "coefficient")


class OutfitItem5ListSerializer(serializers.ModelSerializer):
    outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)
    total_coefficient = SpecificGravityOfLengthSerializer()
    item5 = Item5Serializer(many=True)
    item7 = Item7Serializer(many=True)

    class Meta:
        model = OutfitItem5
        fields = ("id", "outfit", "total_coefficient", "item5", "item7")


class FormAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormAnalysis
        fields = ("id", "name", "date_from", "date_to", "coefficient")


class FormAnalysisDetailSerializer(serializers.ModelSerializer):
    coefficient_item5 = OutfitItemSerializer()
    coefficient_item7 = OutfitItemSerializer()

    class Meta:
        model = FormAnalysis
        fields = ("id", "coefficient_item5", "coefficient_item7", "average_coefficient", "coefficient")


class Item5UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item5
        fields = ("id", "outfit_period_of_time", "length")


class Item7UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item7
        fields = ("id", "total_object", "corresponding_norm")


class Item5CreateSerializer(serializers.ModelSerializer):
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=MainLineType.objects.all())

    class Meta:
        model = Item5
        fields = ("id", "outfit_period_of_time", "length", "type_line")


class Item7CreateSerializer(serializers.ModelSerializer):
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=MainLineType.objects.all())

    class Meta:
        model = Item7
        fields = ("id", "total_object", "corresponding_norm", "type_line")