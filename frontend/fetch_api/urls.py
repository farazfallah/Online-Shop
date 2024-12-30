from django.urls import path
from .request_view import base
from .views import HomeView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('category/<int:id>/', category_detail_view, name='category-detail'),
    # path('product/<int:id>/', product_detail_view, name='product-detail'),
]