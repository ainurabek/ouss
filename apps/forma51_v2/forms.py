from django import forms
from apps.forma51_v2.models import Forma

class Forma51Form(forms.ModelForm):
    class Meta:
    	model = Forma
    	fields = ('object', 'direction', 'amount_inst_channels',
    		'amount_inv_channels', 'year', 'reserve', 'region',
    		'order', 'customer', 'category')