import requests
import json
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages


def product_detail(request, product_id):
    api_url = f"{settings.API_BASE_URL}products/{product_id}/"
    
    try:
        response = requests.get(api_url, proxies={"http": None, "https": None})
        if response.status_code != 200:
            raise Http404("محصول یافت نشد.")
            
        product_data = response.json()
        
        discount = product_data.get('discount', 0)
        price = float(product_data.get('price', 0))
        final_price = price - (price * discount / 100)
        product_data['final_price'] = round(final_price, 2)
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                requested_quantity = int(data.get('quantity', 1))
            except json.JSONDecodeError:
                requested_quantity = int(request.POST.get('count', 1))
            
            if requested_quantity > product_data.get('stock_quantity', 0):
                messages.error(request, f'موجودی محصول {product_data.get("stock_quantity")} عدد است.')
                return HttpResponseRedirect(request.path)

            cart_api_url = f"{settings.API_BASE_URL}cart/"
            cookies = {
                'access_token': request.COOKIES.get('access_token'),
                'cart': request.COOKIES.get('cart')
            }
            
            current_cart = requests.get(
                cart_api_url,
                cookies=cookies,
                proxies={"http": None, "https": None}
            ).json()
            
            current_quantity = 0
            if 'items' in current_cart:
                for item in current_cart['items']:
                    if str(item['product']) == str(product_id):
                        current_quantity = item['quantity']
                        break
            
            if (current_quantity + requested_quantity) > product_data.get('stock_quantity', 0):
                messages.error(
                    request, 
                    f'شما در حال حاضر {current_quantity} عدد از این محصول در سبد خرید دارید. '
                    f'مجموع سفارش نمی‌تواند بیشتر از {product_data.get("stock_quantity")} عدد باشد.'
                )
                return HttpResponseRedirect(request.path)
            
            cart_response = requests.post(
                cart_api_url,
                json={
                    'product': product_id,
                    'quantity': requested_quantity
                },
                cookies=cookies,
                proxies={"http": None, "https": None},
                allow_redirects=False  # Prevent automatic redirects
            )

            if cart_response.status_code in [200, 201]:
                messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد')
                
                redirect_response = HttpResponseRedirect(request.path)
                
                # Directly use the cart data from the response
                cart_data = cart_response.json()
                if 'items' in cart_data:
                    redirect_response.set_cookie(
                        'cart', 
                        json.dumps(cart_data), 
                        httponly=True
                    )
                
                return redirect_response
            
            else:
                error_data = cart_response.json()
                messages.error(request, error_data.get('error', 'خطا در افزودن به سبد خرید'))
        
        return render(request, 'product/product_detail.html', {'product': product_data})
        
    except requests.exceptions.RequestException as e:
        messages.error(request, "خطا در برقراری ارتباط با سرور.")
        return HttpResponseRedirect(request.path)