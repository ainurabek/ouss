from django.contrib import admin
from .models import Object, IP, Point, Outfit, LineType, TPO, TypeOfLocation, TypeOfTrakt, Category, OutfitWorker, MainLineType, AmountChannel, Bug



class IpInline(admin.StackedInline):
    model = IP
    can_delete = True
    verbose_name_plural = 'ИП'
    extra = 0


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    inline = IpInline
    list_display = ('id', 'point', 'name', 'tpo', 'id_outfit')
    search_fields = ('point',)


@admin.register(TPO)
class TPOAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')
    search_fields = ('name',)


class PointInline(admin.StackedInline):
    model = Point
    can_delete = True
    verbose_name_plural = 'Point'
    extra = 0


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ('id', 'outfit', 'adding', 'tpo', 'type_outfit')
    search_fields = ('outfit',)


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_parent', 'name', 'point1', 'point2', 'amount_channels', 'total_amount_channels', 'is_main')
    search_fields = ('name',)


@admin.register(MainLineType)
class MainLineTypeAdmin(admin.ModelAdmin):
    list_display = ('id', "name",)
    search_fields = ('name',)


@admin.register(AmountChannel)
class AmountChannelAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "value", "is_read_only")
    search_fields = ('name',)


admin.site.register(TypeOfTrakt)
admin.site.register(TypeOfLocation)
admin.site.register(LineType)
admin.site.register(Category)
admin.site.register(IP)
admin.site.register(OutfitWorker)
admin.site.register(Bug)

