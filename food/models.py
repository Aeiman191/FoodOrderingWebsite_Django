from pickle import FALSE
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from geopy.geocoders import Nominatim
import datetime

class UserProfile(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        address = models.CharField(max_length=70)
        phone = models.CharField(max_length=14,default='03001234567')
        city = models.CharField(max_length=10,default='Islamabad')

        def __str__(self):
            return self.user.username

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=10)
    lat = models.CharField(max_length=20 , null=True , blank=True)
    lon = models.CharField(max_length=20 , null=True , blank=True)
    
    
    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(self.zipcode))
        self.lat = location.latitude
        self.lon = location.longitude
        super(Restaurant, self).save(*args, **kwargs)
                 
    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField()
    product_image = models.CharField(max_length=70)
    description = models.CharField(max_length=500 , default= 'Order now')
    Restaurant_name = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True ,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False ,null=True ,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    def shipping(self):
        shipping = FALSE
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.cart_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.cart_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 
        

class shippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True , null=True)
    order = models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=70)
    city = models.CharField(max_length=70)

    def __str__(self):
        return self.address


