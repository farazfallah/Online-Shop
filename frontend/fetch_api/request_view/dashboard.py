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

    addresses = profile_data.get('addresses', [])
    return render(request, 'account/address.html', {'addresses': addresses})

