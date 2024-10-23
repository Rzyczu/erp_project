from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=64)
    ean = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    place = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.sku} - {self.name}"
