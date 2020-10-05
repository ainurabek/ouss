from rest_framework import serializers

from apps.dispatching.models import Event, HistoricalEvent

from apps.dispatching.serializers import EventObjectSerializer, EventCircuitSerializer
from apps.opu.objects.serializers import IPListSerializer
from rest_framework.fields import ReadOnlyField

from apps.analysis.models import Punkt5


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

class Punkt5CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Punkt5
        fields = ("id", "name", "total_outfit_region_kls", "total_outfit_region_kls")

class Punkt5Serializer(serializers.ModelSerializer):

    class Meta:
        model = Punkt5
        fields = ("__all__")
        depth=1