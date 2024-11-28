# customer/models.py
from django.db import models
from core.models import BaseModel


class Customer(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True, default='users/default.jpg')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line}, {self.city}"
