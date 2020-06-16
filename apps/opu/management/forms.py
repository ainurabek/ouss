from django import forms

from apps.opu.objects.models import Object

from apps.opu.circuits.models import Circuit


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'system',
                  'amount_channels', 'type_line', 'our', 'num', 'trakt', 'customer' )


class TraktForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'type_of_trakt', 'system',
                  'amount_channels', 'our', 'num', 'trakt', 'customer')

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
                  'amount_channels', 'our', 'num', 'trakt', 'customer')


class ObjectFilterForm(forms.ModelForm):
    q = forms.CharField(label='Название')

    class Meta:
        model = Object
        fields = ('name', 'id_outfit', 'tpo1', 'point1',
                  'tpo2', 'point2', 'type_of_trakt', 'system',
                  'amount_channels', 'our', 'num', 'trakt', 'type_line', 'customer')

    def __init__(self, *args, **kwargs):
        super(ObjectFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class CircuitsEditForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ('final_destination', 'type_using', 'num_order',
                  'date_order', 'num_arenda', 'speed', 'measure', 'adding', 'comments',
                  'in_out', 'first', 'point1',
                  'point2', 'customer', 'mode', 'type_com')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.category = validated_data.get('category', instance.category)
        instance.point1 = validated_data.get('point1', instance.point1)
        instance.point2 = validated_data.get('point2', instance.point2)
        instance.save()
        return instance

