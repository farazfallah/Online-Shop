from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import now
from customers.models import Customer
from customers.utils import send_email

@shared_task
def deactivate_unverified_customers():
    three_days_ago = now() - timedelta(days=3)
    unverified_customers = Customer.objects.filter(
        is_otp_verified=False, 
        is_active=True, 
        date_joined__lte=three_days_ago
    )
    unverified_customers.update(is_active=False)
    return f"{unverified_customers.count()} unverified customers deactivated."



@shared_task
def send_nightly_email():
    users = Customer.objects.filter(is_active=True)

    for user in users:
        try:
            send_email(
                'اطلاعیه شبانه فروشگاه',
                f'سلام {user.first_name} {user.last_name} عزیز\n\n'
                'این یک ایمیل اطلاع‌رسانی شبانه از فروشگاه ما است.\n',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")