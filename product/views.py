from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'product/index.html'