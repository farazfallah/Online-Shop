"""
URL configuration for onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from product.views import HomeView
from core.api import SiteInfoViewSet
from customers.api import (
    LoginWithOtpView, 
    LoginWithPasswordView, 
    RequestOtpView, 
    RegisterView, 
    ValidateTokenView,
    LogoutView,
    CustomerProfileView,
    AddAddressView,
    EditAddressView,
    DeleteAddressView
    )
from product.api import (
    CategoryViewSet,
    AttributeViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductCommentViewSet,
    ProductAttributeViewSet,
    ProductCommentAPIView,
    ProductSearchView
)
from orders.api import (
    CartView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('account/', include('customers.urls')),
    path('order/', include('orders.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='productimage')
router.register(r'product-comments', ProductCommentViewSet, basename='productcomment')
router.register(r'product-attributes', ProductAttributeViewSet, basename='productattribute')

apipath = [
    # Site Info
    path('api/site-info', SiteInfoViewSet.as_view({'get': 'list'}), name='siteinfo'),
    # Auth API
    path('api/login/password/', LoginWithPasswordView.as_view(), name='login_password'),
    path('api/login/otp/request/', RequestOtpView.as_view(), name='request_otp'),
    path('api/login/otp/', LoginWithOtpView.as_view(), name='login_otp'),
    path('api/register/', RegisterView.as_view(), name='register_api'),
    path('api/validate-token/', ValidateTokenView.as_view(), name='validate_token'),
    path('api/logout/', LogoutView.as_view(), name='logout_api'),
    path('api/profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('api/search/', ProductSearchView.as_view(), name='product-search'),
    # Addresses
    path('api/addresses/add/', AddAddressView.as_view(), name='add_address'),
    path('api/addresses/edit/<int:address_id>/', EditAddressView.as_view(), name='edit_address'),
    path('api/addresses/delete/<int:address_id>/', DeleteAddressView.as_view(), name='delete-address'),
    # Comment 
    path('api/products/<int:product_id>/comments/', ProductCommentAPIView.as_view(), name='product-comments'),
    # Cart 
    path('api/cart/', CartView.as_view(), name='cart'), 
    # Product router
    path('api/', include(router.urls)),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += apipath