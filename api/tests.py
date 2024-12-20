from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import Category, Product
from core.models import SiteInfo
from customers.models import Customer

class ApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics")
        cls.product = Product.objects.create(
            name="Smartphone",
            description="A test smartphone",
            price=599.99,
            stock_quantity=10,
            category=cls.category
        )
        cls.site_info = SiteInfo.objects.create(site_name="Test Site", site_email="test@example.com")
        cls.customer = Customer.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_site_info(self):
        url = reverse('siteinfo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_login_with_password(self):
        url = reverse('login_password')
        data_invalid = {"username": self.customer.email, "password": "wrongpassword"}
        response_invalid = self.client.post(url, data_invalid)
        self.assertEqual(response_invalid.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_products_by_category(self):
        url = reverse('products-by-category', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_products(self):
        url = reverse('product-search')
        response = self.client.get(url, {'search': 'Smartphone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)