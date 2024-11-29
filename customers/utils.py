from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Dear User,\n\nYour OTP code is: {otp}\n\nPlease use this code to complete your verification. This code will expire in 3 minutes.\n\nThank you."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
