from django.contrib import admin
from .models import *


class IpInline(admin.StackedInline):
    model = IP
    can_delete = True
    verbose_name_plural = 'ИП'
    extra = 0


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    inlines = (IpInline,)
    list_display = ('id', 'point', 'name', 'tpo', 'id_outfit')
    search_fields = ('point',)


class PointInline(admin.StackedInline):
    model = Point
    can_delete = True
    verbose_name_plural = 'Point'
    extra = 0


admin.site.register(TraktOrLine)
admin.site.register(InOut)
admin.site.register(TPO)
admin.site.register(TypeOfTrakt)
admin.site.register(TypeOfLocation)
admin.site.register(LineType)
admin.site.register(Category)
admin.site.register(System)
# admin.site.register(Point)
admin.site.register(Object)
admin.site.register(IP)
admin.site.register(TransitObject)
admin.site.register(Trassa)
admin.site.register(Outfit)