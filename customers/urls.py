from django.urls import path, include
from customers.api import login_page, register_page, logout_view


urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', logout_view, name='logout'),
]