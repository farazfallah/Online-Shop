from django.urls import path
from fetch_api.request_view import auth
from fetch_api.views import HomeView, login_page, register_page


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/login/', login_page, name='login'),
    path('account/register/', register_page, name='register'),
    path('account/logout/', auth.logout_view, name='logout'),
]