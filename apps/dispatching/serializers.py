from rest_framework import serializers
from apps.dispatching.models import Event
from apps.opu.circuits.models import Circuit
from apps.opu.objects.models import Object, IP
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.objects.models import Object, Point
from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import CircuitList
from apps.dispatching.models import Event
from apps.dispatching.models import TypeOfJournal, Index, Reason
from apps.opu.objects.models import IP, Outfit
from apps.opu.objects.serializers import OutfitListSerializer, ObjectSerializer, IPListSerializer

from apps.opu.circuits.serializers import PointCircSerializer, CategorySerializer
from apps.opu.objects.serializers import TPOSerializer, PointList, TransitSerializer

from apps.opu.circuits.serializers import TransitCircSerializer

from apps.opu.objects.serializers import AllObjectSerializer


class EventObjectSerializer(serializers.ModelSerializer):
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Object
        fields = ('id', "name", "id_outfit", )

class CircuitEventList(serializers.ModelSerializer):
    transit = TransitCircSerializer(many=True, read_only=True)
    transit2 = TransitCircSerializer(many=True, read_only=True)
    point1=PointCircSerializer()
    point2=PointCircSerializer()
    customer = CustomerSerializer()
    category = CategorySerializer()
    id_object = AllObjectSerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'id_object', 'num_circuit', 'type_using', 'category', 'point1', 'point2', 'customer', 'transit', 'transit2')

class ObjectEventSerializer(serializers.ModelSerializer):
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointList()
    point2 = PointList()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)
    id_outfit = OutfitListSerializer()
    category = CategorySerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'category', 'point1', 'point2',
                   'transit', 'transit2', 'tpo1', 'tpo2', 'comments', 'customer')
        depth=1

class EventCircuitSerializer(serializers.ModelSerializer):
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Circuit
        fields = ('id', "name",  )


class IPSSerializer(serializers.ModelSerializer):
    point_id = serializers.SlugRelatedField(slug_field='point', read_only=True)
    object_id = EventObjectSerializer()

    class Meta:
        model = IP
        fields = ( 'id',"point_id", "object_id")
        depth = 1


class EventListSerializer(serializers.ModelSerializer):
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    ips = IPSSerializer()
    index1 = serializers.SlugRelatedField(slug_field='index', read_only=True)
    index2 = serializers.SlugRelatedField(slug_field="index", read_only=True)

    class Meta:
        model = Event
        fields = ('id', "object", "ips", "circuit", "index1", "index2", "date_from", "date_to", 'created_at' )



class TypeJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfJournal
        fields = ('id', 'name',)



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
    type_journal = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeOfJournal.objects.all())
    reason = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Reason.objects.all())
    index1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Index.objects.all())
    index2 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Index.objects.all())
    responsible_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())
    send_from = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())



    class Meta:
        model = Event
        fields = ('id', 'type_journal', 'date_from', 'date_to', 'contact_name',
              'reason', 'index1', 'index2', 'comments', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'created_by')

        depth = 1





class EventDetailSerializer(serializers.ModelSerializer):
    type_journal = TypeJournalSerializer()
    reason=ReasonSerializer()
    index1=IndexSerializer()
    index2 = IndexSerializer()
    responsible_outfit =OutfitListSerializer()
    send_from=OutfitListSerializer()
    ips = IPSSerializer()
    object = EventObjectSerializer()
    circuit=EventCircuitSerializer()
    customer = CustomerSerializer()


    class Meta:
        model = Event
        fields = ('id', 'type_journal',  'date_from', 'date_to', 'contact_name',
              'reason', 'index1', 'index2', 'comments', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'created_by')

