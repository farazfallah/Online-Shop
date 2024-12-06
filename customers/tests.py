from django.test import TestCase
from .models import Customer, Address


class CustomerTest(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create_user(
            email="testuser@example.com",
            password="securepassword",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(str(customer), "Test User")
        self.assertTrue(customer.check_password("securepassword"))


class AddressTest(TestCase):
    def test_create_address(self):
        customer = Customer.objects.create_user(
            email="testuser@example.com",
            password="securepassword",
            first_name="Test",
            last_name="User"
        )
        address = Address.objects.create(
            customer=customer,
            address_line="123 Main St",
            city="Testville",
            state="TS",
            postal_code="12345"
        )
        self.assertEqual(str(address), "123 Main St, Testville")
