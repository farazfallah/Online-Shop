# customer/models.py
from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.managers import CustomUserManager
from django.core.validators import validate_email
from django.conf import settings


class Customer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True, default='users/default.jpg')
    
    otp = models.CharField(max_length=4, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.IntegerField(default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    otp_is_active = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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
