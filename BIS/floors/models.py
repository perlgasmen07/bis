from django.db import models
from buildings.models import Building, User
# Create your models here.
class Floor(models.Model):
    level = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField()
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

class Room(models.Model):
    room_no = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField()
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
