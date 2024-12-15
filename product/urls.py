from django.urls import path
from .views import HomeView, category_detail_view, product_detail_view, ProductDetailAPIView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<str:name>/', category_detail_view, name='category-detail'),
    path('product/<str:name>/', product_detail_view, name='product-detail'),
    path('api/product/<str:name>/', ProductDetailAPIView.as_view(), name='product-detail-api'),
]