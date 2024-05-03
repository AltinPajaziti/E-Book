from django.db import models
from django.contrib.auth.models import User

class Slide(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(null=True, blank=True, upload_to='slides/')

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    discount = models.IntegerField(default=0)
    description = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='products/')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    total = models.FloatField(default=0.0)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_products')