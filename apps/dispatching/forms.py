from django import forms
from .models import ShutdownLog, Request


class ShutdownFilterForm(forms.ModelForm):
    q = forms.CharField(label='Название')

    class Meta:
        model = ShutdownLog
        fields = ('shutdown_type', 'region',
              'status', 'shutdown_periods_from',
              'shutdown_periods_to', 'сause', 'created_by')

    def __init__(self, *args, **kwargs):
        super(ShutdownFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields =('first_name', 'last_name', 'address', 'status', 'type_request',
              'description', 'created_by',)