from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from customers.models import Customer

@shared_task
def deactivate_unverified_customers():
    three_days_ago = now() - timedelta(days=3)
    
    unverified_customers = Customer.objects.filter(
        is_otp_verified=False,
        is_active=True,
        date_joined__lte=three_days_ago
    )
    
    unverified_customers.update(is_active=False)
    
    return f"{unverified_customers.count()} customers deactivated."
