from django import forms
from django.core.exceptions import ValidationError
from .models import Building

class BuildingForms(forms.ModelForm):
    class Meta:
        model = Building
        exclude = ['inserted_by', 'is_deleted', 'deleted_by']
        #fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        shortname = cleaned_data.get('shortname')

        if Building.objects.filter(shortname=shortname).exists():
            raise ValidationError({'shortname': 'A building with this shortname already exists in the college.'})

        return cleaned_data