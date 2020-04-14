from django import forms

from apps.objects.models import TPO, Outfit, Point, Object
from django.forms import inlineformset_factory, modelformset_factory

from apps.form51.models import Form51


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'system',
                  'amount_channels', 'type_line', 'our', 'num', 'trakt', )

class TraktForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'type_of_trakt', 'system',
                  'amount_channels', 'our', 'num', 'trakt',)

    def __init__(self, *args, **kwargs):
        id_parent = kwargs.pop('id_parent')
        super(TraktForm, self).__init__(*args, **kwargs)
        lp = Object.objects.get(id=id_parent)
        self.instance.id_parent = lp

class TraktEditForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'type_of_trakt', 'system',
                  'amount_channels', 'our', 'num', 'trakt', )

class ObjectFilterForm(forms.ModelForm):
    q = forms.CharField(label='Название')

    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'type_of_trakt', 'system',
                  'amount_channels', 'our', 'num', 'trakt', 'type_line',)

    def __init__(self, *args, **kwargs):
        super(ObjectFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class Form51Form(forms.ModelForm):
    class Meta:
        model = Form51
        fields = ('trassa', 'num', 'direction', 'customer',
                  'object', 'point1', 'point2', 'type_line', 'amount_inst_channels', 'amount_inv_channels', 'year',
                  'order', 'schema', 'reserve', )


class Form51FilterForm(forms.ModelForm):
    class Meta:
        model = Form51
        fields = ('trassa', 'num', 'direction', 'customer',
                  'object', 'point1', 'point2', 'type_line', 'amount_inst_channels', 'amount_inv_channels', 'year',
                  'order', 'schema', 'reserve', )
