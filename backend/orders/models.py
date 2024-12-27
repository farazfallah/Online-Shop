# orders/models.py
from django.db import models
from core.models import BaseModel


class Order(BaseModel):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('confirmed', 'Awaiting Confirmation'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.OneToOneField('customers.Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='registered')

    def __str__(self):
        return f"Order {self.id} by {self.customer} ({self.get_status_display()})"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product.name} in Order {self.order.id}"


class DiscountCode(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
