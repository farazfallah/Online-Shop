from django.urls import path
from fetch_api.request_view import auth, category_products, dashboard
from fetch_api.views import HomeView, login_page, register_page


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<int:category_id>/', category_products.category_products, name='category-detail'),
    
    path('account/', dashboard.dashboard_home, name='dashboard-home'),
    path('account/address', dashboard.dashboard_address, name='dashboard-address'),
    path('account/login/', login_page, name='login'),
    path('account/register/', register_page, name='register'),
    path('account/logout/', auth.logout_view, name='logout'),
]