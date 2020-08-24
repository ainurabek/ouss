from django.contrib import admin
from apps.dispatching.models import *


admin.site.register(TypeOfJournal)
admin.site.register(Index)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'index1', 'date_from')
    search_fields = ('created_at',)
admin.site.register(Reason)
admin.site.register(Comments)


