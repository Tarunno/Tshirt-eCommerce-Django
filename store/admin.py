from django.contrib import admin
from . models import *

admin.site.register(Category);
admin.site.register(Customer);
admin.site.register(Product);
admin.site.register(Order);
admin.site.register(OrderItem);
admin.site.register(Shipping);
admin.site.register(Rating);
admin.site.register(Review);
