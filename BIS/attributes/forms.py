from django import forms
from .models import Attribute, Property, BuildingAttribute
import json

class AttributeForms(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = ['inserted_by', 'updated_by', 'deleted_by', 'is_deleted' ]
        #fields = '__all__'

class PropertyForms(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['data', 'updated_by', 'inserted_by', 'is_deleted', 'deleted_by']
    
    def __init__(self, *args, **kwargs):
        super(PropertyForms, self).__init__(*args, **kwargs)
        
        self.fields['attribute'].queryset = Attribute.objects.filter(type='dynamic')
        
class BuildingAttributeForms(forms.ModelForm):
    class Meta:
        model = BuildingAttribute
        exclude = ['attribute', 'inserted_by', 'updated_by', 'is_deleted', 'deleted_by']