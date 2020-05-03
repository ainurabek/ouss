from apps.alarm_log.models import ShutdownLog
from django import forms


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