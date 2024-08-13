from django import forms
from .models import Attribute, Property

class AttributeForms(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = '__all__'

class PropertyForms(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'