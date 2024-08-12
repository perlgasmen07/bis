from django.db import models
from django.db.models import JSONField
from core.models import User
from buildings.models import Building
# Create your models here.
class Attribute(models.Model):
    TYPE_CHOICES=[
        ('static', 'Static'),
        ('dyanmic', 'Dynamic'),
    ]
    shortname = models.CharField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, null=True, blank=True)
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField()
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

class BuildingAttribute(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)  # Nullable value
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.building.shortname} - {self.attribute.shortname}'

class AttributeHistory(models.Model):
    building_attribute = models.ForeignKey(BuildingAttribute, on_delete=models.CASCADE)
    previous_value = models.CharField(max_length=255, blank=True, null=True)  # For static attributes
    new_value = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History of {self.building_attribute}'

class Property(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)  # Nullable JSON data
    inserted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.building.shortname} - {self.attribute.shortname}'
    
class PropertyHistory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    previous_data = JSONField(blank=True, null=True)
    new_data = JSONField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History of {self.property}'