from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from customers.models import Customer
from customers.utils import (
    store_otp_in_redis, 
    send_otp_email,
    generate_otp, 
    delete_otp_from_redis, 
    get_otp_from_redis)


class LoginWithPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response({"error": "حساب کاربری شما غیرفعال شده است."}, status=403)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            login(request, user)

            if user.is_staff:
                return Response({"token": token, "redirect_url": reverse_lazy('admin:index')}, status=200)
            else:
                return Response({"token": token, "redirect_url": reverse_lazy('home')}, status=200)
        else:
            return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=401)


class OtpRequestThrottle(AnonRateThrottle):
    rate = '3/min'


class RequestOtpView(APIView):
    throttle_classes = [OtpRequestThrottle]
    def post(self, request):
        email = request.data.get('email')
        try:
            customer = Customer.objects.get(email=email)
            otp_code = generate_otp()
            store_otp_in_redis(email, otp_code)
            send_otp_email(customer.email, otp_code)
            return Response({'message': 'OTP به ایمیل شما ارسال شد'})
        except Customer.DoesNotExist:
            return Response({'error': 'کاربری با این ایمیل یافت نشد'}, status=status.HTTP_404_NOT_FOUND)


class LoginWithOtpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            customer = Customer.objects.get(email=email)
            stored_otp = get_otp_from_redis(email)  # بازیابی OTP از Redis

            if stored_otp and stored_otp == otp:
                delete_otp_from_redis(email)  # حذف OTP از Redis پس از استفاده
                refresh = RefreshToken.for_user(customer)

                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })

            return Response({'error': 'کد تایید اشتباه است یا منقضی شده است'}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({'error': 'کاربری با این ایمیل یافت نشد'}, status=status.HTTP_404_NOT_FOUND)



def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    return render(request, 'customers/login.html')