from django.contrib import admin
from apps.dispatching.models import *
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(TypeOfJournal)
admin.site.register(Index)

class SimpleHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "name", "instance"]
    history_list_display = ["history_id", 'history_changed_fields']
    search_fields = ['name', 'user__username']



@admin.register(Event)
class EventAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'created_at', 'index1', 'date_from', 'id_parent', 'previous', 'responsible_outfit')
    search_fields = ('created_at',)
admin.site.register(Reason)
admin.site.register(Comments)
admin.site.register(HistoricalEvent)


