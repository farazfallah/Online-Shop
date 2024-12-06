from django.contrib import admin
from .models import Order, OrderItem, DiscountCode


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'customer__email', 'shipping_address__address')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code',)
    ordering = ('-created_at',)
