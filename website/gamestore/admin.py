from django.contrib import admin
from .models import Games, Order, OrderItem
# Register your models here.

# class ItemAdmin(admin.ModelAdmin):
#     list_display = [
#        'title',
#        'price',
#        'discount_price'
#     ]

admin.site.register(Games)
admin.site.register(Order)
admin.site.register(OrderItem)