from django.test import TestCase
from orders.models import Order, OrderItem, DiscountCode
from customers.models import Customer, Address
from product.models import Product
from django.utils.timezone import now


class OrderTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.address = Address.objects.create(
            customer=self.customer,
            address_line="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            country="Test Country"
        )
        self.product = Product.objects.create(
            name="Laptop",
            price=1000.00,
            stock_quantity=10
        )
        self.order = Order.objects.create(
            customer=self.customer,
            shipping_address=self.address,
            total_price=1200.00
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=1000.00
        )
        self.discount_code = DiscountCode.objects.create(
            code="SAVE10",
            discount_percentage=10.00
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.total_price, 1200.00)

    def test_order_item_relation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 1)

    def test_discount_code_creation(self):
        self.assertTrue(DiscountCode.objects.filter(code="SAVE10").exists())

    def test_logical_delete_order(self):
        self.order.delete()
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
        self.assertTrue(Order.objects_with_deleted.filter(id=self.order.id).exists())
