from django.contrib import admin
from .models import Games, Order, OrderItem

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('game_title',)}  # Adjusted field name
    list_display = ['game_title', 'game_price', 'game_discount_price']  # Adjusted field names

admin.site.register(Games, ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
