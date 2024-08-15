from django import forms
from django.core.exceptions import ValidationError
from .models import College

class CollegeForms(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['inserted_by', 'is_deleted', 'deleted_by']
        #fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        shortname = cleaned_data.get('shortname')

        if College.objects.filter(shortname=shortname).exists():
            raise ValidationError({'shortname': 'A college with this shortname already exists in the university.'})

        return cleaned_data