# coding: utf-8
from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Measure, Speed, Mode, Type, SubsRoutes, Circuit, Bypass, AssignPart

admin.site.register(Measure)
admin.site.register(Speed)
admin.site.register(Type)
admin.site.register(SubsRoutes)
admin.site.register(Circuit)
admin.site.register(Bypass)
admin.site.register(AssignPart)
admin.site.register(Mode)