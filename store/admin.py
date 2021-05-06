from django.contrib import admin
from . models import *

admin.site.register(Category)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'image', 'on_sell', 'on_stock', 'delivery']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_placed', 'order_packed', 'order_shipping', 'order_shipped', 'complete', 'date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'id', 'product', 'quentity']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'review', 'date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product', 'user']

admin.site.register(Shipping)
