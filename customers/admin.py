from django.contrib import admin
from .models import Customer, Address

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'image')
    search_fields = ('email', 'phone')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line', 'city', 'state', 'postal_code')
    search_fields = ('name',)
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
