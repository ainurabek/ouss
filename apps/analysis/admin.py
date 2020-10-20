from django.contrib import admin
from apps.analysis.models import *


@admin.register(FormAnalysis)
class FormAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_parent', 'name', "date_from", "date_to", 'outfit', 'average_coefficient', "coefficient",
                    "tv_coefficient")


@admin.register(Punkt5)
class Punkt5Admin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', "outfit", "user")


@admin.register(TotalData)
class TotalDataAdmin(admin.ModelAdmin):
    list_display = ('id', "total_length", "total_coefficient", "kls", "vls", "rrl")


@admin.register(Punkt7)
class Punkt5Admin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', "outfit", "user")
