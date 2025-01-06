from django.shortcuts import render
from django.conf import settings
from django.http import Http404
import requests

def category_products(request, category_id):
    api_url = f'{settings.API_BASE_URL}search/'
    category_check_url = f'{settings.API_BASE_URL}categories/{category_id}/'
    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    page_size = settings.PRODUCTS_PER_PAGE

    # دریافت اطلاعات کتگوری
    try:
        category_response = requests.get(category_check_url)
        category_response.raise_for_status()
        category_data = category_response.json()
        category_name = category_data.get('name', 'دسته‌بندی ناشناخته')
    except requests.RequestException:
        raise Http404("دسته‌بندی مورد نظر یافت نشد.")

    params = {
        'category': category_id,
        'page': page,
        'page_size': page_size,
    }

    if ordering:
        params['ordering'] = ordering

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        products = data.get('results', [])
        total_count = data.get('count', 0)
        total_pages = (total_count + page_size - 1) // page_size 

        pagination = {
            'count': total_count,
            'next': data.get('next'),
            'previous': data.get('previous'), 
            'current_page': page, 
            'page_range': list(range(1, total_pages + 1)),
        }

        product_count_in_page = len(products)

        # محاسبه قیمت نهایی برای محصولات
        for product in products:
            original_price = float(product['price'])
            discount = product['discount']
            if discount > 0:
                final_price = original_price * (1 - discount / 100)
            else:
                final_price = original_price
            product['final_price'] = round(final_price, 2)

    except requests.RequestException as e:
        products = []
        pagination = {
            'count': 0,
            'next': None,
            'previous': None,
            'current_page': 1,
            'page_range': [],
        }
        product_count_in_page = 0
        total_count = 0
        print(f"Error fetching data from API: {e}")

    return render(
        request,
        'product/category_products.html',
        {
            'products': products,
            'pagination': pagination,
            'product_count': total_count,
            'product_count_in_page': product_count_in_page,
            'current_ordering': ordering,
            'category_name': category_name,  # اضافه کردن نام کتگوری به کانتکست
            'category_data': category_data,  # اضافه کردن کل اطلاعات کتگوری به کانتکست
        }
    )