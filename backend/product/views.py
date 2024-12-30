from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from product.models import Product, Category, ProductAttribute
from decimal import Decimal


class HomeView(TemplateView):
    template_name = 'product/index.html'
   

def category_detail_view(request, id):
    category = get_object_or_404(Category, id=id)
    products = category.products.filter(is_active=True)
    subcategories = category.subcategories.filter(is_active=True)
    product_count = products.count()

    for product in products:
        final_price = Decimal(product.price) * (1 - Decimal(product.discount) / 100)
        product.final_price = f"{final_price.normalize():f}"
        product.price = f"{product.price.normalize():f}"
        
    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
        'product_count': product_count,
    }
    return render(request, 'product/category_items.html', context)


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id, is_active=True)
    final_price = Decimal(product.price) * (1 - Decimal(product.discount) / 100)
    product.final_price = f"{final_price.normalize():f}"
    product.price = f"{product.price.normalize():f}"
    
    breadcrumb_items = ['خانه']
    current_category = product.category

    while current_category.parent_category:
        breadcrumb_items.append(current_category.parent_category.name)
        current_category = current_category.parent_category

    breadcrumb_items.append(product.name)

    product_attributes = ProductAttribute.objects.filter(product=product, is_active=True)
    
    similar_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:10]
    
    for similar_product in similar_products:
        final_price = Decimal(similar_product.price) * (1 - Decimal(similar_product.discount) / 100)
        similar_product.final_price = f"{final_price.normalize():f}"
        similar_product.price = f"{similar_product.price.normalize():f}"

    context = {
        'product': product,
        'breadcrumbs': breadcrumb_items,
        'product_attributes': product_attributes,
        'similar_products': similar_products,
    }

    return render(request, 'product/product.html', context)

