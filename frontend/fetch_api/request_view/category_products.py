from django.shortcuts import render
from django.conf import settings
import requests

def category_products(request, category_id):
    api_url = f'{settings.API_BASE_URL}search/'
    page = request.GET.get('page', 1)  # شماره صفحه را از پارامتر GET می‌گیریم
    params = {
        'category': category_id,
        'page': page,
        'page_size': 10,  # تعداد محصولات در هر صفحه
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        products = data.get('results', [])
        
        # اطلاعات مربوط به صفحه‌بندی
        total_pages = (data.get('count') + 9) // 10  # تعداد کل صفحات (هر صفحه ۱۰ محصول)
        pagination = {
            'count': data.get('count'),  # تعداد کل محصولات
            'next': data.get('next'),    # لینک صفحه بعد
            'previous': data.get('previous'),  # لینک صفحه قبلی
            'current_page': int(page),  # صفحه جاری
            'page_range': list(range(1, total_pages + 1)),  # لیست شماره صفحات
        }

        product_count = 0
        for product in products:
            product_count += 1
            category_name = product['category_name']
            original_price = float(product['price'])
            discount = product['discount']
            if discount > 0:
                final_price = original_price * (1 - discount / 100)
            else:
                final_price = original_price
            product['final_price'] = round(final_price, 2)
    
    except requests.RequestException as e:
        products = []
        pagination = {}
        print(f"Error fetching data from API: {e}")

    return render(request, 'product/category_products.html', {'products': products, 'pagination': pagination, 'product_count': product_count, 'category_name': category_name})
