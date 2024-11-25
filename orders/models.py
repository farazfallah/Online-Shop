# orders/models.py
from django.db import models
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('pending', 'Pending'),
        ('confirmed', 'Awaiting Confirmation'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.OneToOneField('customers.Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='registered')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer} ({self.get_status_display()})"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.product.name} in Order {self.order.id}"


class DiscountCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
