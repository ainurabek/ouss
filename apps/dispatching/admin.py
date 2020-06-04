from django.contrib import admin
from apps.dispatching.models import *


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('type_request', 'address', 'first_name', 'type_of_applicant', 'status')
    list_filter = ('type_request', 'type_of_applicant', 'status', 'created_by')
    search_fields = ('address', 'telephone_number', 'department')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TypeRequest)
class TypeRequestAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TypeOfApplicant)
class TypeOfApplicantAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(ShutdownLog)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('shutdown_type', 'address', 'created_by', 'region', 'status')


@admin.register(ShutdownType)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}