from django.test import TestCase
from customers.models import Customer, Address


class CustomerTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com"
        )
        self.address = Address.objects.create(
            customer=self.customer,
            address_line="456 Another St",
            city="Sample City",
            state="Sample State",
            postal_code="67890",
            country="Sample Country"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "Jane")
        self.assertEqual(self.customer.email, "jane.smith@example.com")

    def test_address_relation(self):
        self.assertEqual(self.address.customer, self.customer)
        self.assertEqual(self.address.city, "Sample City")

    def test_logical_delete_customer(self):
        self.customer.delete()
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())
        self.assertTrue(Customer.objects_with_deleted.filter(id=self.customer.id).exists())
