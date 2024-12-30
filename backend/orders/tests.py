from django.test import TestCase
from .models import Order, OrderItem, DiscountCode
from customers.models import Customer, Address
from product.models import Product, Category


class OrderTest(TestCase):
    def test_create_order(self):
        customer = Customer.objects.create_user(email="test@example.com", password="password", first_name="Test", last_name="User")
        order = Order.objects.create(customer=customer, total_price=100.0, status="registered")
        self.assertEqual(str(order), f"Order {order.id} by {customer} (Registered)")


class OrderItemTest(TestCase):
    def test_create_order_item(self):
        customer = Customer.objects.create_user(email="test@example.com", password="password", first_name="Test", last_name="User")
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", category=category, price=599.99, stock_quantity=50)
        order = Order.objects.create(customer=customer, total_price=599.99, status="registered")
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=599.99)
        self.assertEqual(str(order_item), f"Item {product.name} in Order {order.id}")


class DiscountCodeTest(TestCase):
    def test_create_discount_code(self):
        discount = DiscountCode.objects.create(code="DISCOUNT10", discount_percentage=10)
        self.assertEqual(str(discount), "DISCOUNT10")
        self.assertTrue(discount.is_active)