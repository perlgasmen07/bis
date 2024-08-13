from django import forms
from .models import Floor, Room

class FloorForms(forms.ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomForms(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'