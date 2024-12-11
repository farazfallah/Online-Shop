from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Customer

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
                return Response({"token": token, "redirect_url": "/admin/"}, status=200)
            else:
                return Response({"token": token, "redirect_url": "/"}, status=200)
        else:
            return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=401)


class LoginWithOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({"error": "کاربری با این ایمیل یافت نشد."}, status=404)

        # اگر OTP ارسال نشده باشد (درخواست برای ارسال OTP)
        if not otp:
            if not customer.is_active:
                return Response({"error": "حساب کاربری غیرفعال است."}, status=403)

            if customer.otp_is_active:
                return Response({"error": "قبلاً کد تایید ارسال شده است. چند دقیقه صبر کنید."}, status=400)

            # تولید OTP
            generated_otp = get_random_string(length=4, allowed_chars="0123456789")
            customer.otp = generated_otp
            customer.otp_expiry = datetime.now() + timedelta(minutes=5)
            customer.otp_is_active = True
            customer.save()

            # ارسال ایمیل
            send_mail(
                "کد تایید ورود",
                f"کد تایید شما: {generated_otp}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            return Response({"message": "کد تایید به ایمیل ارسال شد."}, status=200)

        # اعتبارسنجی OTP
        if customer.otp != otp or datetime.now() > customer.otp_expiry:
            return Response({"error": "کد تایید نامعتبر یا منقضی است."}, status=400)

        # ورود موفقیت‌آمیز
        customer.otp = None
        customer.otp_expiry = None
        customer.otp_is_active = False
        customer.save()

        # تولید JWT
        refresh = RefreshToken.for_user(customer)
        return Response(
            {"token": str(refresh.access_token), "message": "ورود موفقیت‌آمیز."},
            status=200,
        )



def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))

# @api_view(["POST"])
# def login_with_otp(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         otp = request.data.get('otp')
#         try:
#             user = Customer.objects.get(email=email)
#             if user.otp == otp and user.otp_expiry and user.otp_expiry >= now():
#                 user.otp_is_active = True
#                 user.otp = None
#                 user.otp_expiry = None
#                 user.save()
#                 login(request, user)
#                 redirect_url = '/admin/' if user.is_staff or user.is_superuser else '/'
#                 return JsonResponse({'message': 'Login successful', 'redirect': redirect_url}, status=200)
#             else:
#                 return JsonResponse({'error': 'کد وارد شده اشتباه یا منقضی شده است.'}, status=400)
#         except Customer.DoesNotExist:
#             return JsonResponse({'error': 'کاربر با این ایمیل یافت نشد.'}, status=404)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



# @api_view(["POST"])
# def resend_otp(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         try:
#             user = Customer.objects.get(email=email)
#             otp = random.randint(1000, 9999)
#             user.otp = otp
#             user.otp_expiry = now() + timedelta(minutes=3)
#             user.save()
#             send_otp_email(user.email, otp)
#             return JsonResponse({'message': 'OTP sent successfully'}, status=200)
#         except Customer.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


def login_page(request):
    return render(request, 'customers/login.html')