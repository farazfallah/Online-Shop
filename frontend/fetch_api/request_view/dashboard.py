import requests
import json
from django.contrib import messages
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
            # اضافه یا ویرایش آدرس
            address_data = {
                'address_line': request.POST.get('address_line', '').strip(),
                'city': request.POST.get('city', '').strip(),
                'state': request.POST.get('state', '').strip(),
                'postal_code': request.POST.get('postal_code', '').strip(),
            }

            if not all(address_data.values()):
                messages.error(request, 'لطفا همه فیلدها را پر کنید.')
                return redirect('dashboard-address')

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

        return redirect('dashboard-address')

    addresses = profile_data.get('addresses', [])
    return render(request, 'account/address.html', {
        'addresses': addresses,
    })