from django import forms
from django.core.exceptions import ValidationError
from .models import College

class CollegeForms(forms.ModelForm):
    class Meta:
        model = College
        fields = ['shortname', 'description', 'is_deleted']

    def clean_shortname(self):
        shortname = self.cleaned_data.get('shortname')
        existing_college = College.objects.filter(shortname=shortname).exclude(id=self.instance.id).first()

        if existing_college:
            raise forms.ValidationError("A college with this shortname already exists in the university.")
        
        return shortname