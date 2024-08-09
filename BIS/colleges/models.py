from django.db import models

class College(models.Model):
    shortname = models.CharField(max_length=100)
    description = models.TextField()
    inserted_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name