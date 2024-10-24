from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='custom_groups', blank=True)

    def __str__(self):
        return self.name