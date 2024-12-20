from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views import LoginWithOtpView, LoginWithPasswordView, RequestOtpView, RegisterView
from product.views import ProductCommentAPIView
from api.views import (
    CategoryViewSet,
    AttributeViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductCommentViewSet,
    ProductAttributeViewSet,
    ProductsByCategoryView,
    SiteInfoViewSet,
    ProductSearchView
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
    path('register/', RegisterView.as_view(), name='register_api'),
]

# paths for comments. Not Working for now
comment_urls = [
    path('products/<int:product_id>/comments/', ProductCommentAPIView.as_view(), name='product-comments'),
]

# paths for Search API. Not Working for now
search_api = [
    path('search/', ProductSearchView.as_view(), name='product-search'),
]

category_product_urls = [
    path('category/<int:pk>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
]

urlpatterns = [
    path('', include(router.urls)),
] + auth_urls + comment_urls + search_api + category_product_urls