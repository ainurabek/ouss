from django import forms

from apps.opu.form51.models import Form51


class Form51Form(forms.ModelForm):

    class Meta:
        model = Form51
        fields = ("num_ouss", "reserve", "customer", "report_num",  "reserve_object")

        # "schema", "order",