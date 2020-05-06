from django.contrib import admin

from .models import Region, Form51Location, Form51


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Form51Location)
admin.site.register(Form51)

