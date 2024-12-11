from django.shortcuts import render
# from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from product.models import Product


class HomeView(TemplateView):
    template_name = 'product/index.html'
    
    
class CategoryItemsView(TemplateView):
    template_name = 'product/category_items.html'
    

def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search_results.html', {'query': query, 'results': results})


# def CategoryItemsView(request, slug):
#     category = get_object_or_404(Category, slug=slug)

#     subcategories = category.subcategories.all()
#     categories = [category] + list(subcategories)

#     products = Product.objects.filter(category__in=categories, stock_quantity__gt=0).select_related('category')

#     return render(request, 'product/category_items.html', {
#         'products': products,
#         'category': category,
#         'subcategories': subcategories,
#     })