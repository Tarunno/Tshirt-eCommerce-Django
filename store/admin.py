from django.contrib import admin
from . models import *

admin.site.site_header = "ST Tshirt Shop | admin"

admin.site.register(Category)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'name', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'image', 'on_sell', 'on_stock', 'delivery']
    list_filter = ['on_sell', 'on_stock', 'delivery']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer','custom', 'order_placed', 'order_packed', 'order_shipping', 'order_shipped', 'complete', 'date']
    list_filter = ['order_placed', 'custom']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'id', 'product', 'quentity']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'review', 'date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product', 'user']

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'address', 'city', 'zip', 'state', 'date']

@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'design', 'quentity', 'color', 'tshirt_size', 'design_size', 'date']
