from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'product/index.html'
    
    
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
