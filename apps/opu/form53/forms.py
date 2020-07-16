from django import forms


from apps.opu.form53.models import Form53


class Form53Form(forms.ModelForm):
    class Meta:
        model = Form53
        fields = ('__all__')