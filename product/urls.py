from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<str:category_name>/', CategoryItemsView.as_view(), name='category_items'),
    # path('<str:category_name>/<str:subcategory_name>/', SubcategoryItemsView.as_view(), name='subcategory_items'),
]