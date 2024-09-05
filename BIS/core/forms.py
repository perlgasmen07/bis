from django import forms
from .models import User  # Import your custom User model

class UserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'role')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('groups', None)
        self.fields.pop('user_permissions', None)
        self.fields['is_active'].help_text = None
        self.fields['email'].help_text = None
        self.fields['first_name'].help_text = None
        self.fields['last_name'].help_text = None
