from django import forms
from .models import College

class CollegeForms(forms.ModelForm):
    class Meta:
        model = College
        fields = '__all__'