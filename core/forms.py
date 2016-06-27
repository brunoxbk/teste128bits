from django import forms
from django.utils.translation import ugettext_lazy as _


class FormPeople(forms.Form):
    name = forms.CharField(
        label=_('Name'), required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(
        label=_("Age"), required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    photo = forms.URLField(
        label=_("Photo"), required=True,
        widget=forms.URLInput(attrs={'class': 'form-control'}))
