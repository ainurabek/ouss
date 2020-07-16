from django import forms


from apps.opu.form_customer.models import Form_Customer


class FormCustForm(forms.ModelForm):
    class Meta:
        model = Form_Customer
        fields = ('amount_flow', 'signalization', 'type_of_using', 'num_order', 'comments')

