# coding: utf-8
from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.opu.circuits.models import Circuit, CircuitTransit
User = get_user_model()


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'first', 'is_modified')
    search_fields = ('name',)


@admin.register(CircuitTransit)
class CircuitTransitAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)