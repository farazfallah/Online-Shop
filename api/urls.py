from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views import LoginWithOtpView, LoginWithPasswordView, RequestOtpView
from .views import (
    CategoryViewSet,
    AttributeViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductCommentViewSet,
    ProductAttributeViewSet,
    SiteInfoViewSet,
)

router = DefaultRouter()

# Product
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='productimage')
router.register(r'product-comments', ProductCommentViewSet, basename='productcomment')
router.register(r'product-attributes', ProductAttributeViewSet, basename='productattribute')

# Core
router.register(r'site-info', SiteInfoViewSet, basename='siteinfo')

# paths for authentication
auth_urls = [
    path('login/password/', LoginWithPasswordView.as_view(), name='login_password'),
    path('login/otp/request/', RequestOtpView.as_view(), name='request_otp'),
    path('login/otp/', LoginWithOtpView.as_view(), name='login_otp'),
]

urlpatterns = [
    path('', include(router.urls)),
] + auth_urls
