import requests
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.urls import reverse_lazy

def logout_view(request):
    # آدرس API لاگ‌اوت
    api_logout_url = f'{settings.API_BASE_URL}/api/logout/'
    
    # ارسال درخواست به API
    try:
        response = requests.post(
            api_logout_url,
            cookies=request.COOKIES,
            headers={'X-CSRFToken': request.COOKIES.get('csrftoken')},
        )
        
        # بررسی وضعیت پاسخ API
        if response.status_code == 200:
            # کاربر را از جنگو نیز خارج کنید
            django_logout(request)
            # هدایت به صفحه لاگین
            return redirect(reverse_lazy('login'))
        else:
            return JsonResponse({'error': 'Logout failed on API'}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': 'Error communicating with API', 'details': str(e)}, status=500)
