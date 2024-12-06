from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Address

class CustomerAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line', 'city', 'state', 'postal_code')
    list_filter = ('city', 'state')
    search_fields = ('customer__email', 'address_line', 'city', 'state', 'postal_code')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
