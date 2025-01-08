import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy

def logout_view(request):
    api_logout_url = f'{settings.API_BASE_URL}logout/'
    
    try:
        response = requests.post(
            api_logout_url,
            cookies=request.COOKIES,
            headers={'X-CSRFToken': request.COOKIES.get('csrftoken')},
        )
        
        if response.status_code == 200:
            response = redirect(reverse_lazy('login'))
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            response.delete_cookie('cart')
            return response
        else:
            return JsonResponse({'error': 'Logout failed on API'}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': 'Error communicating with API', 'details': str(e)}, status=500)
    
    