from django.urls import path, include
from customers.api import login_page, register_page, LogoutView


urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
]