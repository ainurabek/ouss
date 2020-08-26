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
from apps.dispatching.models import TypeOfJournal, Index, Reason, Comments
from apps.opu.objects.models import IP, Outfit, OutfitWorker
from apps.opu.objects.serializers import OutfitListSerializer, ObjectSerializer, IPListSerializer

from apps.opu.circuits.serializers import PointCircSerializer, CategorySerializer
from apps.opu.objects.serializers import TPOSerializer, PointList, TransitSerializer

from apps.opu.circuits.serializers import TransitCircSerializer

from apps.opu.objects.serializers import AllObjectSerializer, OutfitWorkerListSerializer

from apps.accounts.serializers import UserLogSerializer

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', "name")

#venet obj detail - Ainur
class EventObjectSerializer(serializers.ModelSerializer):
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_line= serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Object
        fields = ('id', "name", 'id_outfit', 'point1', 'point2', 'type_line', 'amount_channels')

class EventUnknownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', "name", 'responsible_outfit', 'send_from', 'point1', 'point2', 'customer', 'index1', 'index2',
                  'comments1', 'comments2')

class EventDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['event_obj', ]
        depth=2

class CircuitEventList(serializers.ModelSerializer):
    transit = TransitCircSerializer(many=True, read_only=True)
    transit2 = TransitCircSerializer(many=True, read_only=True)
    point1 = PointCircSerializer()
    point2 = PointCircSerializer()
    customer = CustomerSerializer()
    category = CategorySerializer()
    id_object = AllObjectSerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'name', 'id_object', 'num_circuit', 'type_using', 'category', 'point1', 'point2', 'customer', 'transit', 'transit2')

class CircuitDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ['event_cir']
        depth=1

#obj event
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
                   'transit', 'transit2', 'tpo1', 'tpo2', 'customer')
        depth=1

class EventCircuitSerializer(serializers.ModelSerializer):
    point1=serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)


    class Meta:
        model = Circuit
        fields = ('id', "name", 'point1', 'point2')


class IPSSerializer(serializers.ModelSerializer):
    point_id = serializers.SlugRelatedField(slug_field='point', read_only=True)
    object_id = EventObjectSerializer()

    class Meta:
        model = IP
        fields = ( 'id',"point_id", "object_id")
        depth = 1

class IPDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ['event_ips']
        depth=1

#event list
class EventListSerializer(serializers.ModelSerializer):
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    ips = IPSSerializer()
    index1 = serializers.SlugRelatedField(slug_field='index', read_only=True)
    index2 = serializers.SlugRelatedField(slug_field="index", read_only=True)

    class Meta:
        model = Event
        fields = ('id', "object", "ips", "circuit", "index1", "index2", "date_from", "date_to", 'created_at', 'name')

        depth=1



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
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    contact_name = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=OutfitWorker.objects.all())


    class Meta:
        model = Event
        fields = ('id', 'type_journal', 'date_from', 'date_to', 'contact_name',
              'reason', 'index1', 'index2', 'comments1', 'comments2', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'name', 'customer',  'created_at', 'created_by', 'point1', 'point2')

        depth = 2




# class EventDetailSerializer(serializers.ModelSerializer):
#
#     ips = IPDetailObjectSerializer()
#     object = EventDetailObjectSerializer()
#     circuit=CircuitDetailObjectSerializer()
#
#     class Meta:
#         model = Event
#         fields = ('object', 'circuit', 'ips' )
#         depth=2

#event detail
class EventDetailSerializer(serializers.ModelSerializer):
    type_journal = TypeJournalSerializer()
    reason = ReasonSerializer()
    index1 = IndexSerializer()
    index2 = IndexSerializer()
    responsible_outfit = OutfitListSerializer()
    send_from = OutfitListSerializer()
    ips = IPSSerializer()
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    customer = CustomerSerializer()
    created_by = UserLogSerializer()
    point1 = serializers.SlugRelatedField(slug_field="point", read_only=True)
    point2 = serializers.SlugRelatedField(slug_field="point", read_only=True)
    contact_name=OutfitWorkerListSerializer()


    class Meta:
        model = Event
        fields = ('id', 'type_journal',  'date_from', 'date_to', 'contact_name',
              'reason', 'index1', 'index2', 'comments1', 'comments2', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer',  'created_at', 'created_by', 'point1', 'point2', 'name')