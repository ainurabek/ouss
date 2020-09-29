from rest_framework import serializers

from apps.dispatching.models import Event, HistoricalEvent

from apps.dispatching.serializers import EventObjectSerializer, EventCircuitSerializer
from apps.opu.objects.serializers import IPListSerializer
from rest_framework.fields import ReadOnlyField




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
        fields = ('id', 'history_id', "history_date", "changed_field",
                  "history_user", 'history_type')
        depth = 1
