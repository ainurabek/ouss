# coding: utf-8
from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Measure, Speed, Mode, TypeCom, Circuit

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'first')
    search_fields = ('name',)

admin.site.register(Measure)
admin.site.register(TypeCom)
admin.site.register(Mode)