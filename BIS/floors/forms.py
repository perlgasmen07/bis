from django import forms
from django.core.exceptions import ValidationError
from .models import Floor, Room

class FloorForms(forms.ModelForm):
    class Meta:
        model = Floor
        exclude = ['inserted_by', 'is_deleted', 'deleted_by']
        #fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        building = cleaned_data.get('building')

        if Floor.objects.filter(level=level, building=building).exists():
            raise ValidationError({'level': 'A floor with this level already exists in the building.'})

        return cleaned_data

class RoomForms(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['inserted_by', 'is_deleted', 'deleted_by']

    def clean(self):
        cleaned_data = super().clean()
        room_no = cleaned_data.get('room_no')
        floor = cleaned_data.get('floor')

        if Room.objects.filter(room_no=room_no, floor=floor).exists():
            raise ValidationError({'room_no': 'A room with this number already exists on this floor.'})

        return cleaned_data