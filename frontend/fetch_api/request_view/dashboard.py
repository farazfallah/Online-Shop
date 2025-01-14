import requests
import json
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect, render
from .utils import fetch_customer_profile

def dashboard_home(request):
    profile_data = fetch_customer_profile(request)
    if profile_data is None:
        return redirect('login')

    context = {
        'first_name': profile_data.get('first_name'),
        'last_name': profile_data.get('last_name'),
        'email': profile_data.get('email'),
        'phone': profile_data.get('phone'),
        'is_otp_verified': profile_data.get('is_otp_verified')
    }
    return render(request, 'account/dashboard.html', context)


def dashboard_address(request):
    profile_data = fetch_customer_profile(request)
    if profile_data is None:
        return redirect('login')

    if request.method == 'POST':
        address_id = request.POST.get('address_id', '').strip()

        if 'delete_address' in request.POST:
            token = request.COOKIES.get('access_token')
            if not token:
                messages.error(request, 'لطفا دوباره وارد شوید.')
                return redirect('login')

            try:
                response = requests.delete(
                    f'{settings.API_BASE_URL}addresses/delete/{address_id}/',
                    headers={
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                )

                if response.status_code == 204:
                    messages.success(request, 'آدرس با موفقیت حذف شد!')
                else:
                    response_data = response.json()
                    error_msg = response_data.get('detail', 'خطا در حذف آدرس')
                    messages.error(request, error_msg)

            except Exception as e:
                messages.error(request, f'خطا در ارتباط با سرور: {str(e)}')

        else:
            address_data = {
                'address_line': request.POST.get('address_line', '').strip(),
                'city': request.POST.get('city', '').strip(),
                'state': request.POST.get('state', '').strip(),
                'postal_code': request.POST.get('postal_code', '').strip(),
            }

            if not all(address_data.values()):
                messages.error(request, 'لطفا همه فیلدها را پر کنید.')
                return redirect('dashboard_address')

            token = request.COOKIES.get('access_token')
            if not token:
                messages.error(request, 'لطفا دوباره وارد شوید.')
                return redirect('login')

            try:
                if address_id:
                    response = requests.put(
                        f'{settings.API_BASE_URL}addresses/edit/{address_id}/',
                        data=json.dumps(address_data),
                        headers={
                            'Authorization': f'Bearer {token}',
                            'Content-Type': 'application/json'
                        }
                    )
                else:
                    response = requests.post(
                        f'{settings.API_BASE_URL}addresses/add/',
                        data=json.dumps(address_data),
                        headers={
                            'Authorization': f'Bearer {token}',
                            'Content-Type': 'application/json'
                        }
                    )

                if response.status_code in [200, 201]:
                    messages.success(request, 'آدرس با موفقیت ذخیره شد!')
                else:
                    response_data = response.json()
                    error_msg = response_data.get('detail', 'خطا در ذخیره آدرس')
                    messages.error(request, error_msg)
            except Exception as e:
                messages.error(request, f'خطا در ارتباط با سرور: {str(e)}')

        return redirect('dashboard_address')

    addresses = profile_data.get('addresses', [])
    return render(request, 'account/address.html', {
        'addresses': addresses,
    })
    

from django.contrib import messages

def customer_profile_page(request):
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            try:
                access_token = request.COOKIES.get('access_token')
                headers = {'Authorization': f'Bearer {access_token}'}
                
                files = {'profile_image': request.FILES['profile_image']}
                response = requests.patch(
                    f'{settings.API_BASE_URL}profile/',
                    headers=headers,
                    files=files,
                    cookies=request.COOKIES
                )
                
                if response.status_code == 200:
                    messages.success(request, "تصویر پروفایل با موفقیت بروزرسانی شد.")
                else:
                    messages.error(request, f"خطا در آپلود تصویر: {response.text}")
                    
            except Exception as e:
                messages.error(request, f"خطای سیستمی: {str(e)}")
        
        else:
            try:
                access_token = request.COOKIES.get('access_token')
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                data = {
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name')
                }
                
                response = requests.patch(
                    f'{settings.API_BASE_URL}profile/',
                    headers=headers,
                    json=data,
                    cookies=request.COOKIES
                )
                
                if response.status_code == 200:
                    messages.success(request, "اطلاعات پروفایل با موفقیت بروزرسانی شد.")
                else:
                    messages.error(request, f"خطا در بروزرسانی پروفایل: {response.text}")
                    
            except Exception as e:
                messages.error(request, f"خطای سیستمی: {str(e)}")
        
        return redirect('profile_page')

    profile_data = fetch_customer_profile(request)
    if profile_data is None:
        return redirect('login')

    return render(request, 'account/edit_profile.html')




def order_list(request):
    profile_data = fetch_customer_profile(request)
    if profile_data is None:
        return redirect('login')
    
    try:
        access_token = request.COOKIES.get('access_token')

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f'{settings.API_BASE_URL}orders/',
            headers=headers
        )

        if response.status_code == 200:
            orders = response.json()
            
            for order in orders:
                created_at = timezone.datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
                order['created_at_formatted'] = created_at.strftime('%Y/%m/%d')
                
            context = {
                'orders': orders,
            }
            
            return render(request, 'account/order_list.html', context)
        elif response.status_code == 401:
            context = {
                'error': 'Authentication failed. Please log in again.',
            }
            return render(request, 'account/order_list.html', context)
        else:
            context = {
                'error': 'Unable to fetch orders',
                'status_code': response.status_code
            }
            return render(request, 'account/order_list.html', context)
    
    except requests.RequestException as e:
        context = {
            'error': f'Network error: {str(e)}',
        }
        return render(request, 'account/order_list.html', context)