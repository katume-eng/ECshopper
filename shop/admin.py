from django.contrib import admin
from .models import Product,CartItem,Order,OrderItem
# Register your models here.

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
