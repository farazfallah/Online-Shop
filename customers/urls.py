from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('login/', login_page, name='login'),
    path('login/password/', LoginWithPasswordView.as_view(), name='login_with_password'),
    path('logout', logout_view, name='logout'),
]