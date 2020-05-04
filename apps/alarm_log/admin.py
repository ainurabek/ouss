from django.contrib import admin
from apps.alarm_log.models import *


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('type_statement', 'address', 'first_name', 'type_of_statement', 'status')
    list_filter = ('type_statement', 'type_of_statement', 'status', 'created_by')
    search_fields = ('address', 'telephone_number', 'specialist')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TypeStatement)
class TypeStatementAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TypeOfStatement)
class TypeOfStatementAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Departament)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ShutdownLog)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('shutdown_type', 'address', 'created_by', 'region', 'status')


@admin.register(ShutdownType)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


