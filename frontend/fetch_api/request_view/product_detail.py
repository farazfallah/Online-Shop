import requests
from django.shortcuts import render
from django.http import Http404
from django.conf import settings


def product_detail(request, product_id):
    api_url = f"{settings.API_BASE_URL}products/{product_id}/"
    try:
        response = requests.get(api_url, proxies={"http": None, "https": None})
        if response.status_code == 200:
            product_data = response.json()
            
            # محاسبه قیمت نهایی پس از تخفیف
            discount = product_data.get('discount', 0)
            price = float(product_data.get('price', 0))
            final_price = price - (price * discount / 100)
            
            # اضافه کردن قیمت نهایی به داده‌ها
            product_data['final_price'] = round(final_price, 2)
            
            return render(request, 'product/product_detail.html', {'product': product_data})
        else:
            raise Http404("محصول یافت نشد.")
    except requests.exceptions.RequestException:
        raise Http404("خطا در برقراری ارتباط با سرور.")
