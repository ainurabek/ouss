from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Object, TPO, Outfit, TypeOfLocation, Point, IP, LineType, TypeOfTrakt, Category, OutfitWorker, \
    AmountChannel, SchemaObjectPhoto, OrderObjectPhoto, Order

from ..circuits.serializers import CategorySerializer
from ..customer.models import Customer
from ..customer.serializers import CustomerSerializer

User = get_user_model()


class PointList(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('id', 'point')

class AmountChannelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AmountChannel
        fields = ("id", "name", 'value')

class LineTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LineType
        fields = ('id', 'name')


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
        fields = ('id', 'point', 'name', 'id_outfit', 'tpo')
        depth = 1


class PointCreateSerializer(serializers.ModelSerializer):
    tpo = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=TPO.objects.all())
    id_outfit = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Outfit.objects.all())

    class Meta:
        model = Point
        fields = ('point', 'name', 'id_outfit', 'tpo')
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
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'point1', 'name', 'point2')

class IPSerializer(serializers.ModelSerializer):
    point_id=serializers.SlugRelatedField(slug_field='point', read_only=True)
    object_id=serializers.SlugRelatedField(slug_field='name', read_only=True)
    tpo_id = serializers.SlugRelatedField(slug_field='index', read_only=True)
    class Meta:
        model = IP
        fields = ('id', 'tpo_id', 'point_id', 'object_id' )

class AllObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = ('__all__')

class LPSerializer(serializers.ModelSerializer):
    transit = TransitSerializer(many=True)
    transit2 = TransitSerializer(many=True)
    point1 = PointList()
    point2 = PointList()
    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'transit', 'transit2', 'num')

class ObjectOrderPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderObjectPhoto
        fields = ("id", "src")

class ObjectSchemaPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaObjectPhoto
        fields = ("id", "src")

class LPDetailSerializer(serializers.ModelSerializer):
    point1 = PointList()
    point2 = PointList()
    type_line = TypeLineSerializer()
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)
    id_outfit = ObjectOutfitSerializer()
    ip_object = IPSerializer(many=True)
    category = CategorySerializer()
    our = TypeOfLocationSerializer()
    customer = CustomerSerializer()
    order_object_photo = ObjectOrderPhotoSerializer(many=True)
    schema_object_photo = ObjectSchemaPhotoSerializer(many=True)
    amount_channels = AmountChannelListSerializer()

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'trakt', 'type_line', 'transit',
                  'transit2', 'tpo1', 'category', 'tpo2', 'id_outfit', 'comments',
                  'customer', 'ip_object', 'our', 'amount_channels', 'num', 'total_amount_channels',
                  'total_amount_active_channels', 'order_object_photo', 'schema_object_photo')

        depth = 1


class LPCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Category.objects.all())
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
    amount_channels = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=AmountChannel.objects.all())

    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'category', 'tpo1', 'point1', 'tpo2', 'point2', 'trakt', 'type_line', 'our',
                  'comments',  'customer', 'amount_channels')


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
    category = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Category.objects.all())
    customer = serializers.PrimaryKeyRelatedField(
        read_only=False, allow_null=True, queryset=Customer.objects.all())



    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'category', 'tpo1', 'point1', 'tpo2', 'point2', 'trakt', 'type_line', 'our',
        'comments', 'customer', 'num')
        depth = 1



class ObjectSerializer(serializers.ModelSerializer):
    id_parent=ParentSerializer()
    tpo1 = TPOSerializer()
    tpo2 = TPOSerializer()
    point1 = PointList()
    point2 = PointList()
    type_of_trakt = TypeOfTraktSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)
    id_outfit = OutfitListSerializer()
    type_line = TypeLineSerializer()
    ip_object = IPSerializer(many=True)
    category = CategorySerializer()
    our = TypeOfLocationSerializer()
    customer = CustomerSerializer()
    order_object_photo = ObjectOrderPhotoSerializer(many=True)
    schema_object_photo = ObjectSchemaPhotoSerializer(many=True)
    amount_channels = AmountChannelListSerializer()

    class Meta:
        model = Object
        fields = ('id', 'id_parent', 'name', 'trakt', 'id_outfit', 'category', 'point1', 'point2',
                  'type_of_trakt', 'transit', 'transit2', 'tpo1', 'tpo2', 'comments', 'customer', 'type_line', 'our',
                  "ip_object", 'num', 'amount_channels', "total_amount_channels", 'total_amount_active_channels',
                  'order_object_photo', 'schema_object_photo')


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

    class Meta:
        model = Object
        fields = ('id', 'id_parent','name', 'id_outfit', 'trakt', 'tpo1',
                  'point1', 'tpo2', 'point2', 'type_of_trakt', 'amount_channels', 'our', 'num',
                  'transit', 'transit2', 'category', 'comments', 'customer')


class SelectObjectSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)


    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt', 'transit', 'transit2')


class ObjectListSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_of_trakt = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt')


class TraktListSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    type_of_trakt = TypeOfTraktSerializer()
    transit = TransitSerializer(many=True, read_only=True)
    transit2 = TransitSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = ('id', 'name', 'point1', 'point2', 'type_of_trakt', "transit", "transit2")


class ObjectFilterSerializer(serializers.ModelSerializer):
    point1 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    point2 = serializers.SlugRelatedField(slug_field='point', read_only=True)
    id_outfit = serializers.SlugRelatedField(slug_field='outfit', read_only=True)

    class Meta:
        model = Object
        fields = ( 'id', 'name', 'point1', 'point2', 'id_outfit', 'customer')




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'name', 'src', 'created_date')

