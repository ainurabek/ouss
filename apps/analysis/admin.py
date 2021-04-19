from django.contrib import admin
from apps.analysis.models import *


@admin.register(FormAnalysis)
class FormAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_parent', 'name', "date_from", "date_to", 'outfit', 'average_coefficient', "coefficient")


@admin.register(Punkt5)
class Punkt5Admin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', "outfit", "user")


@admin.register(TotalData)
class TotalDataAdmin(admin.ModelAdmin):
    list_display = ('id', "total_length", "total_coefficient", "kls", "vls", "rrl")


@admin.register(Punkt7)
class Punkt5Admin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', "outfit", "user")

@admin.register(Form61KLS)
class Form61KLSAdmin(admin.ModelAdmin):
    list_display = ('id', 'point1', 'point2', "outfit", "total_length_line", "total_length_cable",
                    'above_ground', 'under_ground', 'year_of_laying', 'laying_method', 'type_cable', 'type_connection')

@admin.register(TypeConnection)
class Form61KLSAdmin(admin.ModelAdmin):
    list_display = ('id', "name")

@admin.register(TypeCable)
class Form61KLSAdmin(admin.ModelAdmin):
    list_display = ('id', "name")

@admin.register(MethodLaying)
class Form61KLSAdmin(admin.ModelAdmin):
    list_display = ('id', "name")