from django.contrib import admin
from apps.dispatching.models import *


admin.site.register(TypeOfJournal)
admin.site.register(Index)



#Event_admin
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'index1', 'date_from', 'id_parent', 'previous', 'responsible_outfit')
    search_fields = ('created_at',)
admin.site.register(Reason)
admin.site.register(Comments)


