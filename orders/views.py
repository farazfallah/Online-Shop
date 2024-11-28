from django.shortcuts import render
from django.http import HttpResponse

def order_home(request):
    return HttpResponse("Orders Home Page")

