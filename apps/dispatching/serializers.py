from rest_framework import serializers
from apps.opu.customer.serializers import CustomerSerializer
from apps.opu.objects.models import Object, Point
from apps.opu.circuits.models import Circuit
from apps.dispatching.models import Event
from apps.dispatching.models import TypeOfJournal, Index, Reason, Comments
from apps.opu.objects.models import IP, Outfit, OutfitWorker
from apps.opu.objects.serializers import OutfitListSerializer
from apps.opu.objects.serializers import PointList, PointListSerializer
from apps.opu.objects.serializers import OutfitWorkerListSerializer
from apps.accounts.serializers import UserLogSerializer
from apps.opu.objects.serializers import ObjectOutfitSerializer
from apps.opu.form_customer.serializers import EventObjFormCustSerializer, EventCircuitFormCustSerializer



class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', "name")


class TypeJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfJournal
        fields = ('id', "name")


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', "name", 'is_read_only')


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('id', 'index', "name", 'is_read_only')


#event obj detail - Ainur
class EventObjectSerializer(serializers.ModelSerializer):
    id_outfit = ObjectOutfitSerializer()
    point1 = PointList()
    point2 = PointList()
    type_line = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Object
        fields = ('id', "name", 'id_outfit', 'point1', 'point2', 'type_line', 'amount_channels')


class EventDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['event_obj', ]
        depth=2


class CircuitDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ['event_cir']
        depth=1

#obj event - Ainur


class EventCircuitSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Circuit
        fields = ('id', "name", 'point1', 'point2')


class IPDetailObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ['event_ips']
        depth=1


#event list - Ainur
class EventListSerializer(serializers.ModelSerializer):
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    ips = PointListSerializer()
    index1 = serializers.SlugRelatedField(slug_field='index', read_only=True)
    responsible_outfit = serializers.SlugRelatedField(slug_field="outfit", read_only=True)

   
    class Meta:
        model = Event
        fields = ('id', "object", "ips", "circuit", "index1", "date_from", "date_to", 'created_at', 'time_created_at', 'name',
                  "responsible_outfit")
        depth=1


class EventCreateSerializer(serializers.ModelSerializer):
    """Создания события"""
    type_journal = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeOfJournal.objects.all())
    reason = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Reason.objects.all())
    index1 = serializers.PrimaryKeyRelatedField(
        read_only=False,  queryset=Index.objects.all())

    responsible_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False,  queryset=Outfit.objects.all())
    send_from = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    contact_name = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=OutfitWorker.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'type_journal', 'date_from', 'date_to', 'contact_name', 'reason', 'index1', 'comments1',
                  'responsible_outfit', 'send_from', 'object', 'circuit', 'ips', 'name', 'customer',  'created_at',
                  'time_created_at', 'created_by', 'point1', 'point2', 'calculate')

        depth = 2


class CallsCreateSerializer(serializers.ModelSerializer):
    """Создания события"""
    type_journal = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeOfJournal.objects.all())
    reason = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Reason.objects.all())
    index1 = serializers.PrimaryKeyRelatedField(
        read_only=False,  queryset=Index.objects.all())

    responsible_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False,  queryset=Outfit.objects.all())
    send_from = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Point.objects.all(), allow_empty=True)
    contact_name = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=OutfitWorker.objects.all())
    object = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Object.objects.all(), allow_null=True)
    ips = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all(), allow_null=True)
    circuit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Circuit.objects.all(), allow_null=True)

    class Meta:
        model = Event
        fields = ('id', 'type_journal', 'date_from', 'date_to', 'contact_name', 'reason', 'index1', 'comments1',
                  'responsible_outfit', 'send_from', 'object', 'circuit', 'ips', 'name', 'customer',  'created_at',
                  'time_created_at', 'created_by', 'point1', 'point2', 'calculate')
        depth = 2


#event detail - Ainur
class EventDetailSerializer(serializers.ModelSerializer):
    type_journal = TypeJournalSerializer()
    reason = ReasonSerializer()
    index1 = IndexSerializer()
    responsible_outfit = OutfitListSerializer()
    send_from = OutfitListSerializer()
    ips = PointListSerializer()
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    customer = CustomerSerializer()
    created_by = UserLogSerializer()
    point1 = PointList()
    point2 = PointList()
    contact_name=OutfitWorkerListSerializer()

    class Meta:
        model = Event
        fields = ('id', 'type_journal',  'date_from', 'date_to', 'contact_name', 'reason', 'index1', 'comments1',
                  'responsible_outfit', 'send_from', 'object', 'circuit', 'ips', 'customer',  'created_at',
                  'time_created_at', 'created_by', 'point1', 'point2', 'name', 'calculate')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date_from', 'date_to', 'index1', 'created_at',  'object', 'circuit', 'ips', 'name')


class DamageReportListSerializer(serializers.ModelSerializer):
    ips = PointListSerializer()
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    responsible_outfit = OutfitListSerializer()
    point1 = PointList()
    point2 = PointList()

    class Meta:
        model = Event
        fields = ("id", "date_from", "date_to", "downtime", "comments1", "arrival_date", "comments1",
                  "responsible_outfit", "ips", "object", "circuit", "point1", "point2")


class DamageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "arrival_date")


class InternationalDamageReportListSerializer(serializers.ModelSerializer):
    ips = PointListSerializer()
    object = EventObjectSerializer()
    circuit = EventCircuitSerializer()
    point1 = PointList()
    point2 = PointList()

    class Meta:
        model = Event
        fields = ("id", "date_from", "date_to", "downtime", "comments1", "arrival_date", "comments1", "ips", "object",
                  "circuit", "point1", "point2")


class TechStopReportListSerializer(serializers.ModelSerializer):
    object = EventObjFormCustSerializer()
    circuit = EventCircuitFormCustSerializer()
    reason = ReasonSerializer

    class Meta:
        model = Event
        fields = ("id", 'index1', "reason", "date_from", "date_to", 'object', 'circuit')