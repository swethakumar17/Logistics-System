from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=70)
    mobile = models.IntegerField(max_length=10)
    address = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name


class Supplier(models.Model):
    SupplierName = models.CharField(max_length=200)
    ContactNumber = models.IntegerField()

    def __str__(self):
        return self.SupplierName


class Product(models.Model):
    SupplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image_url = models.CharField(max_length=500,default="")

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse("cart", id=id)

class Location(models.Model):
    source = models.CharField(max_length=40)
    destination = models.CharField(max_length=40)

    def __str__(self):
        return self.source


class Order_Item(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class Pack(models.Model) :
    user_id = models.IntegerField()
    prod_id = models.IntegerField()
    ordered_date = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    vehicle_id = models.IntegerField()
    source = models.IntegerField()


class Vehicle(models.Model) :
    name = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
