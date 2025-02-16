from django.contrib import admin
from .models import Games, Order, OrderItem, Address

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('game_title',)}  
    list_display = ['game_title', 'game_price', 'game_discount_price']  

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'email',
        'street_address',
        'apartment_address',
        'city',
        'post_code',
        'default'
        ] 


admin.site.register(Games, ItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
