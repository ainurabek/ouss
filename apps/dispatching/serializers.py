from rest_framework import serializers
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.objects.models import Object, Point
from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import CircuitList
from apps.dispatching.models import Event
from apps.dispatching.models import TypeOfJournal, Choice, Index, Reason
from apps.opu.objects.models import IP, Outfit
from apps.opu.objects.serializers import OutfitListSerializer, ObjectSerializer, IPListSerializer


class TypeJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfJournal
        fields = ('id', 'name',)

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'index', 'name',)

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'name',)

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('id', 'index', 'name',)

class EventCreateSerializer(serializers.ModelSerializer):
    """Создания события"""
    choice = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Choice.objects.all())
    reason = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Reason.objects.all())
    index = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Index.objects.all())
    responsible_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    send_from = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    object = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Object.objects.all())
    circuit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=Circuit.objects.all())
    ips = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=IP.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())


    class Meta:
        model = Event
        fields = ('id', 'choice', 'date_from', 'date_to', 'contact_name',
              'reason', 'index', 'comments', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'created_by')

class EventDetailSerializer(serializers.ModelSerializer):
    type_journal = TypeJournalSerializer()
    choice = ChoiceSerializer()
    reason=ReasonSerializer()
    index=IndexSerializer()
    responsible_outfit =OutfitListSerializer()
    send_from=OutfitListSerializer()
    ips = IPListSerializer()
    object = ObjectSerializer()
    circuit=CircuitList()
    customer = CustomerSerializer()


    class Meta:
        model = Event
        fields = ('id', 'type_journal', 'choice', 'date_from', 'date_to', 'contact_name',
              'reason', 'index', 'comments', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'created_by')