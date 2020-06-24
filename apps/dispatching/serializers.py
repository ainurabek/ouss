from rest_framework import serializers

from apps.dispatching.models import Event
from apps.opu.circuits.models import Circuit
from apps.opu.objects.models import Object, IP


class EventObjectSerializer(serializers.ModelSerializer):
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Object
        fields = ("name", "id_outfit", )


class EventCircuitSerializer(serializers.ModelSerializer):
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Circuit
        fields = ("name", "id_outfit", )


class IPSSerializer(serializers.ModelSerializer):
    point_id = serializers.SlugRelatedField(slug_field='point', read_only=True)
    object_id = EventObjectSerializer()

    class Meta:
        model = IP
        fields = ("point_id", "object_id")
        depth = 1


class EventListSerializer(serializers.ModelSerializer):
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    ips = IPSSerializer()
    index = serializers.SlugRelatedField(slug_field="index", read_only=True)

    class Meta:
        model = Event
        fields = ("object", "ips", "circuit", "index", "date_from", "date_to", )
