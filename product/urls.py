from django.urls import path
from .views import HomeView, category_detail_view, product_detail_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<str:name>/', category_detail_view, name='category-detail'),
    path('product/<str:name>/', product_detail_view, name='product-detail'),
    # path('categories/', CategoryProductsListView.as_view(), name='category-products-list'),
    # path('category/<str:name>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('api/categories/<int:category_id>/', CategoryItemsAPIView.as_view(), name='category_items_api'),
    # path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('<str:category_name>/<str:subcategory_name>/', SubcategoryItemsView.as_view(), name='subcategory_items'),
]