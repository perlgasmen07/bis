from django import forms
from .models import Building

class BuildingForms(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'