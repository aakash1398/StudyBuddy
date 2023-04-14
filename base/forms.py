from django import forms
from .models import Room


class Roomform(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'