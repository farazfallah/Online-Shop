from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
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
            response = requests.get(api_url, headers=headers, proxies={"http": None, "https": None})
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
    
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        messages.error(request, 'لطفا ابتدا وارد حساب کاربری خود شوید')
        return redirect('login')
        
    headers['Authorization'] = f"Bearer {access_token}"
    
    # دریافت اطلاعات سبد خرید
    try:
        response = requests.get(api_url, headers=headers, proxies={"http": None, "https": None})
        if response.status_code == 200:
            cart_data = response.json()
            if not cart_data['items']:
                messages.warning(request, 'سبد خرید شما خالی است')
                return redirect('cart')
        elif response.status_code == 401:
            messages.error(request, 'نشست کاربری شما منقضی شده است. لطفا دوباره وارد شوید')
            return redirect('login')
    except requests.RequestException as e:
        print(f"Error fetching cart data: {e}")
        messages.error(request, 'خطا در دریافت اطلاعات سبد خرید')
        return redirect('cart')

    # دریافت لیست آدرس‌ها
    addresses = []
    try:
        addresses_url = f"{settings.API_BASE_URL}addresses/"
        response = requests.get(addresses_url, headers=headers, proxies={"http": None, "https": None})
        if response.status_code == 200:
            addresses = response.json()
    except requests.RequestException as e:
        print(f"Error fetching addresses: {e}")
        messages.error(request, 'خطا در دریافت لیست آدرس‌ها')

    # دریافت پیش‌نمایش فاکتور
    checkout_preview = None
    try:
        checkout_url = f"{settings.API_BASE_URL}checkout/"
        response = requests.get(checkout_url, headers=headers, proxies={"http": None, "https": None})
        if response.status_code == 200:
            checkout_preview = response.json()
        elif response.status_code == 400:
            data = response.json()
            messages.error(request, data.get('error', 'خطا در دریافت اطلاعات فاکتور'))
            return redirect('cart')
    except requests.RequestException as e:
        print(f"Error fetching checkout preview: {e}")
        messages.error(request, 'خطا در دریافت اطلاعات فاکتور')
        return redirect('cart')

    if request.method == 'POST':
        address_id = request.POST.get('delivery_address')
        if not address_id:
            messages.error(request, 'لطفا یک آدرس را انتخاب کنید')
        else:
            try:
                # یافتن آدرس انتخاب شده
                selected_address = next(
                    (addr for addr in addresses if str(addr['id']) == str(address_id)), 
                    None
                )
                
                if not selected_address:
                    messages.error(request, 'آدرس انتخاب شده معتبر نیست')
                    return redirect('checkout')

                # ارسال شناسه آدرس به جای اطلاعات آدرس
                checkout_url = f"{settings.API_BASE_URL}checkout/"
                response = requests.post(
                    checkout_url, 
                    headers=headers,
                    json={
                        'address_id': address_id,  # تغییر از shipping_address به address_id
                        'discount_code': request.POST.get('discount_code')
                    },
                    proxies={"http": None, "https": None}
                )
                
                if response.status_code == 201:
                    messages.success(request, 'سفارش شما با موفقیت ثبت شد')
                    return redirect('order_list')
                else:
                    data = response.json()
                    error_message = data.get('error', 'خطا در ثبت سفارش')
                    messages.error(request, error_message)
                    
            except requests.RequestException as e:
                print(f"Error creating order: {e}")
                messages.error(request, 'خطا در ارتباط با سرور')

    context = {
        "cart": cart_data,
        "addresses": addresses,
        "checkout_preview": checkout_preview,
    }
    
    return render(request, "cart/checkout.html", context)
