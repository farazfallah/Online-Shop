import requests
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'product/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            response = requests.get(f'{settings.API_BASE_URL}products/')
            response.raise_for_status()
            
            data = response.json()
            products = data.get('results', [])
            
            for product in products:
                discount = product.get('discount', 0)
                price = float(product.get('price', 0))
                final_price = price - (price * discount / 100)
                product['final_price'] = round(final_price, 2)
            
            context['products'] = products
        except requests.RequestException as e:
            context['products'] = []
            context['error'] = str(e)
        return context
    
    
def register_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    
    context = {
    'api_base_url': settings.API_BASE_URL,
    }
    return render(request, 'account/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))

    context = {
        'api_base_url': settings.API_BASE_URL,
    }
    return render(request, 'account/login.html', context)
