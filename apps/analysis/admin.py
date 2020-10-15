from django.contrib import admin
from apps.analysis.models import *


@admin.register(FormAnalysis)
class FormAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_parent', 'name', "date_from", "date_to", 'outfit', 'average_coefficient', "coefficient")


@admin.register(Item5)
class Item5Admin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', 'outfit_period_of_time', 'length', "type_line", "outfit_item5")


@admin.register(OutfitItem5)
class OutfitItem5Admin(admin.ModelAdmin):
    list_display = ('id', "id_parent", "outfit", "total_coefficient")


@admin.register(SpecificGravityOfLength)
class SpecificGravityOfLengthAdmin(admin.ModelAdmin):
    list_display = ('id', "total_length", "coefficient")


@admin.register(SpecificGravityOfLengthTypeLine)
class SpecificGravityOfLengthTypeLineAdmin(admin.ModelAdmin):
    list_display = ('id', "type_line", "value", "specific_gravity_of_length")


admin.site.register(Item7)

