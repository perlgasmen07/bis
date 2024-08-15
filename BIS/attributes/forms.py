from django import forms
from .models import Attribute, Property
import json

class AttributeForms(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = ['inserted_by', 'updated_by', 'deleted_by', 'is_deleted' ]
        #fields = '__all__'

class PropertyForms(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['data', 'updated_by', 'inserted_by']
    
    def __init__(self, *args, **kwargs):
        super(PropertyForms, self).__init__(*args, **kwargs)
        
        # Filter attributes to only include those that are 'dynamic'
        self.fields['attribute'].queryset = Attribute.objects.filter(type='dynamic')
        
    #     # Initialize dynamic fields based on existing attribute-related keys
    #     if 'attribute' in self.initial:
    #         attribute = self.initial['attribute']
    #         self.load_existing_keys(attribute)

    # def load_existing_keys(self, attribute):
    #     # Load existing keys related to the attribute (mocked for demonstration)
    #     existing_keys = {
    #         'key1': 'value1',
    #         'key2': 'value2',
    #         # This should be replaced with actual logic to fetch keys related to the attribute
    #     }

    #     for key, value in existing_keys.items():
    #         self.fields[key] = forms.CharField(initial=value, label=key)

    #     # Adding an additional field to add more keys
    #     self.fields['new_key'] = forms.CharField(required=False, label="Add a new key")

    # def clean(self):
    #     cleaned_data = super().clean()
        
    #     # Handle additional keys
    #     new_key = cleaned_data.get('new_key')
    #     if new_key:
    #         # Add logic to handle new key-value pairs
    #         cleaned_data[new_key] = "default_value"  # Set default value or get from the user input
        
    #     return cleaned_data