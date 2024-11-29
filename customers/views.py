from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Customer
from .utils import send_otp_email
import random
from datetime import timedelta



@csrf_exempt
def login_with_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            redirect_url = '/admin/' if user.is_staff or user.is_superuser else '/'
            return JsonResponse({'message': 'Login successful', 'redirect': redirect_url}, status=200)
        else:
            return JsonResponse({'error': 'ایمیل یا رمز عبور اشتباه است.'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(["POST"])
def login_with_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = Customer.objects.get(email=email)
            if user.otp == otp and user.otp_expiry and user.otp_expiry >= now():
                user.otp_is_active = True
                user.otp = None
                user.otp_expiry = None
                user.save()
                login(request, user)
                redirect_url = '/admin/' if user.is_staff or user.is_superuser else '/'
                return JsonResponse({'message': 'Login successful', 'redirect': redirect_url}, status=200)
            else:
                return JsonResponse({'error': 'کد وارد شده اشتباه یا منقضی شده است.'}, status=400)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'کاربر با این ایمیل یافت نشد.'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@api_view(["POST"])
def resend_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        try:
            user = Customer.objects.get(email=email)
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.otp_expiry = now() + timedelta(minutes=3)
            user.save()
            send_otp_email(user.email, otp)
            return JsonResponse({'message': 'OTP sent successfully'}, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def login_page(request):
    return render(request, 'customers/login.html')