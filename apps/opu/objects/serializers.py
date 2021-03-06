from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Object, TPO, Outfit, TypeOfLocation, Point, IP, LineType, TypeOfTrakt, Category, OutfitWorker, \
    AmountChannel, OrderObjectPhoto, Consumer, Bug, MainLineType, Transit, Bridge, IPTV
from ..customer.models import Customer
from ..customer.serializers import CustomerSerializer


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'index', 'name')


class BugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bug
        fields = ('id', 'text',)


class PointList(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('id', 'point', 'name')


class AmountChannelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AmountChannel
        fields = ("id", "name", 'value', 'is_read_only')


class MainLineTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainLineType
        fields = ("id", "name")


class LineTypeCreateSerializer(serializers.ModelSerializer):
    main_line_type = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=MainLineType.objects.all())

    class Meta:
        model = LineType
        fields = ('id', 'name', 'main_line_type')


class LineTypeSerializer(serializers.ModelSerializer):
    main_line_type = MainLineTypeListSerializer()

    class Meta:
        model = LineType
        fields = ('id', 'name', 'main_line_type')


class ObjectOutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ('id', 'outfit',)


class TPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPO
        fields = ('id', 'name', 'index')
        depth = 1


class TypeOfLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfLocation
        fields = ('id', 'name',)


class TypeOfTraktSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfTrakt
        fields = ('id', 'name',)


class TypeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineType
        fields = ('id', 'name',)


class OutfitListSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    type_outfit = TypeOfLocationSerializer()

    class Meta:
        model = Outfit
        fields = ('id', 'outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit', 'created_by')
        depth = 1


class OutfitWorkerListSerializer(serializers.ModelSerializer):
    outfit = OutfitListSerializer()

    class Meta:
        model = OutfitWorker
        fields = ('id', 'outfit', 'name')
        depth = 1


class OutfitWorkerCreateSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())

    class Meta:
        model = OutfitWorker
        fields = ('id', 'outfit', 'name')
        depth = 1


class OutfitCreateSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    type_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TypeOfLocation.objects.all())

    class Meta:
        model = Outfit
        fields = ('outfit', 'adding', 'num_outfit', 'tpo', 'type_outfit')
        depth = 1


class PointListSerializer(serializers.ModelSerializer):
    tpo = TPOSerializer()
    id_outfit = OutfitListSerializer()

    class Meta:
        model = Point
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo', 'region', 'type_equipment')
        depth = 1


class PointCreateSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())

    class Meta:
        model = Point
        fields = ('point', 'name', 'id_outfit', 'tpo', 'region', 'type_equipment')
        depth = 1


class IPListSerializer(serializers.ModelSerializer):
    tpo_id = TPOSerializer()
    point_id = PointListSerializer()

    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1


class IPCreateSerializer(serializers.ModelSerializer):
    tpo_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    object_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Object.objects.all())

    class Meta:
        model = IP
        fields = ('id', 'point_id', 'object_id', 'tpo_id')
        depth = 1


class ParentSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2')


class TransitSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()

    class Meta:
        model = Object
        fields = ('id', 'point1', 'name', 'point2')


class IPSerializer(serializers.ModelSerializer):
    point_id = serializers.SlugRelatedField(slug_field='point', read_only=True)
    object_id = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tpo_id = serializers.SlugRelatedField(slug_field='index', read_only=True)

    class Meta:
        model = IP
        fields = ('id', 'tpo_id', 'point_id', 'object_id' )


class OrderObjectPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderObjectPhoto
        fields = ("id", "src")


class TransitListSerializer(serializers.ModelSerializer):
    trassa = TransitSerializer(many=True)

    class Meta:
        model = Transit
        fields = ("id", "name", "trassa")


class BridgeListSerializer(serializers.ModelSerializer):
    transit = TransitListSerializer()

    class Meta:
        model = Bridge
        fields = ("transit", )


class BridgeSerializer(serializers.ModelSerializer):
    object = TransitSerializer()

    class Meta:
        model = Bridge
        fields = ("object", )


class TransitDetailSerializer(serializers.ModelSerializer):
    trassa = TransitSerializer(many=True)
    can_see = BridgeSerializer(many=True)

    class Meta:
        model = Transit
        fields = ("id", "name", "trassa", "can_see", "create_circuit_transit")



class AllObjectSerializer(serializers.ModelSerializer):
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointList()
    point2 = PointList()
    bridges = BridgeListSerializer(many=True)
    id_outfit = OutfitListSerializer()
    category = CategorySerializer()
    customer = CustomerSerializer()



    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'category', 'point1', 'point2', 'tpo1', 'tpo2', 'customer', 'bridges', 'form_cust_obj')
        depth = 1


class LPSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2')


class LPDetailSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    type_line = TypeLineSerializer()
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    bridges = BridgeListSerializer(many=True)
    id_outfit = ObjectOutfitSerializer()
    ip_object = IPSerializer(many=True)
    our = TypeOfLocationSerializer()
    customer = CustomerSerializer()
    order_object_photo = OrderObjectPhotoSerializer(many=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_line', 'tpo1', 'tpo2', 'id_outfit', 'comments',
                  'customer', 'ip_object', 'our', 'total_amount_channels', 'order_object_photo', 'bridges')
        depth = 1


class LPCreateSerializer(serializers.ModelSerializer):

    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=LineType.objects.all())
    our = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeOfLocation.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'type_line', 'our',
                  'comments',  'customer')


class LPEditSerializer(serializers.ModelSerializer):
    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Point.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=LineType.objects.all())
    our = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeOfLocation.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'name', 'id_outfit', 'tpo1', 'point1', 'tpo2', 'point2', 'type_line', 'our', 'comments',
                  'customer')
        depth = 1


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ('id', 'name')


class ObjectSerializer(serializers.ModelSerializer):
    id_parent = ParentSerializer()
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointList()
    point2 = PointList()
    type_of_trakt = TypeOfTraktSerializer()
    id_outfit = OutfitListSerializer()
    type_line = TypeLineSerializer()
    ip_object = IPSerializer(many=True)
    category = CategorySerializer()
    our = TypeOfLocationSerializer()
    customer = CustomerSerializer()
    consumer = ConsumerSerializer()
    amount_channels = AmountChannelListSerializer()
    order_object_photo = OrderObjectPhotoSerializer(many=True)

    class Meta:
        model = Object
        fields = ('id', 'id_parent', 'name', 'id_outfit', 'category', 'point1', 'point2',
                  'type_of_trakt', 'tpo1', 'tpo2', 'comments', 'customer', 'type_line', 'our',
                  "ip_object",  'amount_channels', "total_amount_channels",'order_object_photo', 'consumer')


class ObjectCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Category.objects.all())
    our = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeOfLocation.objects.all())

    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
         read_only=False, allow_null=True, queryset=Point.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False,  allow_null=True, queryset=TPO.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
         read_only=False, allow_null=True, queryset=Point.objects.all())
    type_of_trakt = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=TypeOfTrakt.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())

    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())
    amount_channels = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=AmountChannel.objects.all())
    consumer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Consumer.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'id_parent','name', 'id_outfit', 'tpo1',
                  'point1', 'tpo2', 'point2', 'type_of_trakt', 'amount_channels', 'our', 'category', 'comments', 'customer', 'consumer')


class ObjectEditSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Category.objects.all())
    our = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TypeOfLocation.objects.all())

    tpo1 = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=TPO.objects.all())
    point1 = serializers.PrimaryKeyRelatedField(
         read_only=False, allow_null=True, queryset=Point.objects.all())
    tpo2 = serializers.PrimaryKeyRelatedField(
        read_only=False,  allow_null=True, queryset=TPO.objects.all())
    point2 = serializers.PrimaryKeyRelatedField(
         read_only=False, allow_null=True, queryset=Point.objects.all())
    type_of_trakt = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True,  queryset=TypeOfTrakt.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())
    consumer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Consumer.objects.all())

    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())
    type_line = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=LineType.objects.all())

    class Meta:
        model = Object
        fields = ('id', 'id_parent','name', 'id_outfit', 'tpo1',
                  'point1', 'tpo2', 'point2', 'type_of_trakt', 'our', 'category', 'comments', 'customer', 'consumer',
                  'type_line')


class SelectObjectSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)


    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt')


class ObjectListSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_of_trakt = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt')


class TraktListSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    type_of_trakt = TypeOfTraktSerializer()
    id_parent = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'id_parent', 'name', 'point1', 'point2', 'type_of_trakt')


class ObjectFilterSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)
    ip_object = IPSerializer(many=True)

    class Meta:
        model = Object
        fields = ( 'id', 'name', 'point1', 'point2', 'id_outfit', 'customer', 'ip_object', 'type_of_trakt')


class PGListSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2')


class GOZListSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer()
    bridges = BridgeListSerializer(many=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'comments_GOZ', 'consumer', 'bridges')


class GOZUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ('id', 'comments_GOZ')


class TransitCreateSerializer(serializers.ModelSerializer):
    trassa = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Object.objects.all(), many=True)

    class Meta:
        model = Transit
        fields = ("id", "name", "trassa", "create_circuit_transit")

class IPTVSerializer(serializers.ModelSerializer):
    outfit = OutfitListSerializer()
    class Meta:
        model = IPTV
        fields = ('id', 'outfit', 'name', 'num_channel', 'ip_address', 'resource', 'comments')

class IPTVCreateSerializer(serializers.ModelSerializer):
    outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Outfit.objects.all())
    class Meta:
        model = IPTV
        fields = ('id', 'outfit', 'name', 'num_channel', 'ip_address', 'resource', 'comments')