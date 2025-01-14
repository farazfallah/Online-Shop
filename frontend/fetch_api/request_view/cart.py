from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json

def cart_view(request):
    api_url = f"{settings.API_BASE_URL}cart/"
    headers = {}
    cart_data = None
    
    access_token = request.COOKIES.get('access_token')
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                cart_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching cart data: {e}")
    
    if not cart_data:
        try:
            cart_cookie = request.COOKIES.get('cart')
            if cart_cookie:
                cart_data = json.loads(cart_cookie)
                total_price = sum(float(item.get('price', 0)) for item in cart_data.get('items', []))
                cart_data['total_price'] = total_price
            else:
                cart_data = {
                    'items': [], 
                    'total_price': 0,
                    'customer': None,
                    'is_active': True
                }
        except json.JSONDecodeError:
            cart_data = {
                'items': [], 
                'total_price': 0,
                'customer': None,
                'is_active': True
            }
        except Exception as e:
            print(f"Error processing cart cookie: {e}")
            cart_data = {
                'items': [], 
                'total_price': 0,
                'customer': None,
                'is_active': True
            }

    return render(request, "cart/cart.html", {"cart": cart_data})


def checkout_view(request):
    api_url = f"{settings.API_BASE_URL}cart/"
    headers = {}
    cart_data = None
    
    # Check if user is authenticated via access token
    access_token = request.COOKIES.get('access_token')
        
    headers['Authorization'] = f"Bearer {access_token}"
    
    # Get cart data first to check if there are items
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            cart_data = response.json()
            if not cart_data['items']:
                return redirect('cart')  # Redirect if cart is empty
    except requests.RequestException as e:
        print(f"Error fetching cart data: {e}")
        return redirect('cart')

    # Get addresses if user is authenticated
    addresses = []
    try:
        addresses_url = f"{settings.API_BASE_URL}customer/addresses/"
        response = requests.get(addresses_url, headers=headers)
        if response.status_code == 200:
            addresses = response.json()
    except requests.RequestException as e:
        print(f"Error fetching addresses: {e}")

    # Get checkout preview
    checkout_preview = None
    try:
        checkout_url = f"{settings.API_BASE_URL}checkout/"
        response = requests.get(checkout_url, headers=headers)
        if response.status_code == 200:
            checkout_preview = response.json()
    except requests.RequestException as e:
        print(f"Error fetching checkout preview: {e}")

    context = {
        "cart": cart_data,
        "addresses": addresses,
        "checkout_preview": checkout_preview,
    }
    
    return render(request, "cart/checkout.html", context)