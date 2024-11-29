from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('login/password/', login_with_password, name='login_with_password'),
    path('login/otp/', login_with_otp, name='login_with_otp'),
    path('resend-otp/', resend_otp, name='resend_otp'),
    path('api-auth/', include('rest_framework.urls'))
]