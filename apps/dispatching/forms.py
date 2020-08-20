from django import forms
from .models import Event




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =('type_journal', 'date_from', 'date_to', 'created_by', 'contact_name',
              'reason', 'index1', 'index2', 'comments1', 'comments2', 'responsible_outfit', 'send_from',
                 'object', 'circuit', 'ips', 'customer')