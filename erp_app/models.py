from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Item(models.Model):
    sku = models.CharField(max_length=64)
    ean = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    place = models.CharField(max_length= 64)
    
    def __str__(self):
        return (f"{self.sku} - {self.name}")
    
    
class User(AbstractBaseUser):
    name = models.CharField(max_length=64, blank=False)
    surname = models.CharField(max_length=64, blank=False)
    login = models.CharField(max_length=64, blank=False, unique=True)
    email = models.EmailField(max_length=64, blank=False, unique=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

    def __str__(self):
        return f"{self.name} {self.surname}"
