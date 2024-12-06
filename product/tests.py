from django.test import TestCase
from .models import Category, Attribute, Product, ProductComment, ProductAttribute


class CategoryTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Electronics", description="Gadgets and devices")
        self.assertEqual(str(category), "Electronics")


class AttributeTest(TestCase):
    def test_create_attribute(self):
        attribute = Attribute.objects.create(name="Color", description="Product color")
        self.assertEqual(str(attribute), "Color")


class ProductTest(TestCase):
    def test_create_product(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Smartphone",
            description="A test smartphone",
            category=category,
            price=599.99,
            stock_quantity=100,
        )
        self.assertEqual(str(product), "Smartphone")
        self.assertEqual(product.category.name, "Electronics")


class ProductCommentTest(TestCase):
    def test_create_comment(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", category=category, price=599.99, stock_quantity=100)
        comment = ProductComment.objects.create(product=product, comment="Great product", rating=5)
        self.assertEqual(str(comment), f"Comment by None on {product}")


class ProductAttributeTest(TestCase):
    def test_create_product_attribute(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Smartphone", category=category, price=599.99, stock_quantity=100)
        attribute = Attribute.objects.create(name="Color")
        product_attribute = ProductAttribute.objects.create(product=product, attribute=attribute, value="Black")
        self.assertEqual(str(product_attribute), "Color: Black for Smartphone")
