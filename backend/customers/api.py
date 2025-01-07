from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from customers.serializers import CustomerSerializer, AddressSerializer
from customers.models import Customer, Address
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
        try:
            customer = Customer.objects.get(email=email)
            if not customer.check_password(password):
                return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=401)

            if not customer.is_active:
                return Response({"error": "حساب کاربری شما غیرفعال شده است."}, status=403)

            refresh = RefreshToken.for_user(customer)
            access_token = str(refresh.access_token)

            response = Response({
                "message": "ورود موفقیت‌آمیز بود.",
                "redirect_url": reverse_lazy('home')
            }, status=200)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,  # Ensures the token is not accessible via JavaScript
                max_age=15 * 60,  # Expiry in seconds (same as your access token lifetime)
                secure=True,  # Use only over HTTPS in production
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                max_age=24 * 60 * 60,
                secure=True,
            )
            return response

        except Customer.DoesNotExist:
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
            stored_otp = get_otp_from_redis(email)

            if stored_otp and stored_otp == otp:
                if not customer.is_otp_verified:
                    customer.is_otp_verified = True
                    customer.save()

                refresh = RefreshToken.for_user(customer)
                access_token = str(refresh.access_token)

                redirect_url = reverse_lazy('home')

                delete_otp_from_redis(email)
                
                response = Response({
                    "message": "ورود موفقیت‌آمیز بود.",
                    "redirect_url": redirect_url
                }, status=200)

                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    max_age=15 * 60,
                    secure=True,
                )
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    max_age=24 * 60 * 60,
                    secure=True,
                )

                return response
            else:
                return Response({'error': 'کد تایید اشتباه است یا منقضی شده است'}, status=status.HTTP_401_UNAUTHORIZED)

        except Customer.DoesNotExist:
            return Response({'error': 'کاربری با این ایمیل یافت نشد'}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        re_password = request.data.get('re_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "فرمت ایمیل نادرست است."}, status=status.HTTP_400_BAD_REQUEST)

        if password != re_password:
            return Response({"error": "رمز عبور و تکرار آن مطابقت ندارند."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        if Customer.objects.filter(email=email).exists():
            return Response({"error": "ایمیل وارد شده قبلاً ثبت شده است."}, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return Response({"message": "ثبت‌نام با موفقیت انجام شد."}, status=status.HTTP_201_CREATED)


class ValidateTokenView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not access_token:
            return Response({
                'error': 'توکن دسترسی یافت نشد',
                'is_valid': False
            }, status=401)
            
        try:
            access_token_obj = AccessToken(access_token)
            user_id = access_token_obj.payload.get('user_id')
            
            customer = Customer.objects.get(id=user_id)
            return Response({
                'is_valid': True,
                'user': {
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'phone': customer.phone,
                    'image_url': request.build_absolute_uri(customer.image.url) if customer.image else None,
                    'is_staff': customer.is_staff,
                    'is_active': customer.is_active,
                    'is_otp_verified': customer.is_otp_verified,
                }
            })
            
        except TokenError:
            if not refresh_token:
                return Response({
                    'error': 'نیاز به لاگین مجدد دارید',
                    'is_valid': False
                }, status=401)
                
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                new_access_token = str(refresh_token_obj.access_token)
                
                user_id = refresh_token_obj.payload.get('user_id')
                customer = Customer.objects.get(id=user_id)
                
                response = Response({
                    'is_valid': True,
                    'user': {
                        'email': customer.email,
                        'first_name': customer.first_name,
                        'last_name': customer.last_name,
                        'phone': customer.phone,
                        'image_url': request.build_absolute_uri(customer.image.url) if customer.image else None,
                        'is_staff': customer.is_staff,
                        'is_active': customer.is_active,
                        'is_otp_verified': customer.is_otp_verified,
                    }
                })
                
                response.set_cookie(
                    key='access_token',
                    value=new_access_token,
                    httponly=True,
                    max_age=15 * 60,
                    secure=True,
                    samesite='Lax'
                )
                
                return response
                
            except TokenError:
                return Response({
                    'error': 'نیاز به لاگین مجدد دارید',
                    'is_valid': False
                }, status=401)
                
        except Customer.DoesNotExist:
            return Response({
                'error': 'کاربر یافت نشد',
                'is_valid': False
            }, status=404)


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user 
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class AddAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = request.user
        data = request.data
        
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, address_id):
        customer = request.user
        try:
            # بررسی اینکه آدرس متعلق به کاربر فعلی است
            address = Address.objects.get(id=address_id, customer=customer)
        except Address.DoesNotExist:
            return Response({'detail': 'آدرس موردنظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        # بررسی داده‌های ورودی
        data = request.data
        serializer = AddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, address_id):
        customer = request.user
        try:
            address = Address.objects.get(id=address_id, customer=customer)
        except Address.DoesNotExist:
            return Response({'detail': 'آدرس موردنظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({'detail': 'آدرس با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)



def register_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    return render(request, 'customers/register.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    return render(request, 'customers/login.html')


class LogoutView(APIView):
   def post(self, request):
       response = Response({'message': 'با موفقیت خارج شدید.'})
       response.delete_cookie('access_token')
       response.delete_cookie('refresh_token')
       logout(request)
       return response