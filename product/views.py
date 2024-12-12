from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from product.models import Product, Category, ProductAttribute
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.generics import ListAPIView
from decimal import Decimal, ROUND_HALF_UP

class HomeView(TemplateView):
    template_name = 'product/index.html'
   
    
def category_detail_view(request, name):
    category = get_object_or_404(Category, name=name)
    products = category.products.filter(is_active=True)
    subcategories = category.subcategories.all()
    product_count = products.count()
    
    for product in products:
        product.final_price = Decimal(product.price) * (1 - Decimal(product.discount)/100)

    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
        'product_count': product_count,
    }
    return render(request, 'product/category_items.html', context)


def product_detail_view(request, name):
    product = get_object_or_404(Product, name=name)
    product.final_price = Decimal(product.price) * (1 - Decimal(product.discount)/100)
    
    breadcrumb_items = ['خانه']
    current_category = product.category

    while current_category.parent_category:
        breadcrumb_items.append(current_category.parent_category.name)
        current_category = current_category.parent_category

    breadcrumb_items.append(product.name)

    product_attributes = ProductAttribute.objects.filter(product=product)
    
    context = {
        'product': product,
        'breadcrumbs': breadcrumb_items,
        'product_attributes': product_attributes,
    }
    
    return render(request, 'product/product.html', context)
