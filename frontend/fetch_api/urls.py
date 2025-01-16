from django.urls import path
from fetch_api.request_view import auth, category_products, dashboard, product_detail, search, cart
from fetch_api.views import HomeView, login_page, register_page


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<int:category_id>/', category_products.category_products, name='category-detail'),
    path('products/<int:product_id>/', product_detail.product_detail, name='product_detail'),    
    path('search/', search.search_view, name='search_results'),
    
    path('cart/', cart.cart_view, name='cart'),
    path('cart/checkout/', cart.checkout_view, name='checkout'),
    
    path('account/', dashboard.dashboard_home, name='dashboard-home'),
    path('account/profile/', dashboard.customer_profile_page, name='profile_page'),
    path('account/address', dashboard.dashboard_address, name='dashboard_address'),
    path('account/orders', dashboard.order_list, name='order_list'),
    path('account/orders/<int:order_id>/', dashboard.order_detail, name='order_detail'),
    path('account/login/', login_page, name='login'),
    path('account/register/', register_page, name='register'),
    path('account/logout/', auth.logout_view, name='logout'),
]