from django.contrib import admin
from .models import UserProfile , Restaurant , Products, shippingAddress,order,cart


admin.site.register(UserProfile)
admin.site.register(Restaurant)
admin.site.register(Products)
admin.site.register(order)
admin.site.register(cart)
admin.site.register(shippingAddress)

