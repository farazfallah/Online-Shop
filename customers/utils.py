from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import random

def store_otp_in_redis(email, otp_code, expiration_minutes=5):
    cache_key = f"otp:{email}"
    cache.set(cache_key, otp_code, timeout=timedelta(minutes=expiration_minutes).total_seconds())

def get_otp_from_redis(email):
    cache_key = f"otp:{email}"
    return cache.get(cache_key)

def delete_otp_from_redis(email):
    cache_key = f"otp:{email}"
    cache.delete(cache_key)
    
def send_otp_email(customer_email, otp_code):
    subject = "Your OTP Code"
    message = f"Dear user,\n\nYour OTP code is: {otp_code}\n\nThis code is valid for 5 minutes. Please do not share it with anyone."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email]

    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f"Error sending OTP email: {e}")

def generate_otp():
    return str(random.randint(100000, 999999))