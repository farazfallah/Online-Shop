from django.db import models
from core.models import BaseModel, LogicalDeleteModel


class Order(BaseModel, LogicalDeleteModel):
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


class OrderItem(BaseModel, LogicalDeleteModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='order_items')
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product_name} in Order {self.order.id}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.product_name = self.product.name
            self.product_price = self.product.price
        super().save(*args, **kwargs)


class DiscountCode(BaseModel, LogicalDeleteModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    

class Cart(BaseModel):
    customer = models.ForeignKey(
        'customers.Customer', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='carts'
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.customer:
            return f"Cart of {self.customer}"
        return f"Cart (Session: {self.session_id})"

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.URLField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in Cart {self.cart.id}"
