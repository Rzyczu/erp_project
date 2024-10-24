from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, through='TeamUserRole', related_name='teams', blank=True)


    def __str__(self):
        return self.name