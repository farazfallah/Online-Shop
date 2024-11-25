from django.test import TestCase
from product.models import Product, Category, Attribute, ProductAttribute, ProductComment
from customers.models import Customer


class ProductTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.attribute = Attribute.objects.create(name="Color")
        self.product = Product.objects.create(
            name="Smartphone",
            category=self.category,
            price=799.99,
            stock_quantity=5
        )
        self.customer = Customer.objects.create(
            first_name="Alice",
            last_name="Wonder",
            email="alice.wonder@example.com"
        )
        self.product_attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute=self.attribute,
            value="Black"
        )
        self.product_comment = ProductComment.objects.create(
            product=self.product,
            customer=self.customer,
            comment="Great product!",
            rating=5
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.stock_quantity, 5)

    def test_product_attribute(self):
        self.assertEqual(self.product_attribute.attribute.name, "Color")
        self.assertEqual(self.product_attribute.value, "Black")

    def test_product_comment(self):
        self.assertEqual(self.product_comment.comment, "Great product!")
        self.assertEqual(self.product_comment.rating, 5)

    def test_logical_delete_product(self):
        self.product.delete()
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertTrue(Product.objects_with_deleted.filter(id=self.product.id).exists())
