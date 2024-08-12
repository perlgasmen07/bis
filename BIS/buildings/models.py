from django.db import models
from core.models import User

from colleges.models import College

# Create your models here.
class Building(models.Model):
    shortname = models.CharField(max_length=25)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')    
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField()
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.shortname