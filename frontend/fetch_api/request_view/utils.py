from django.conf import settings
import requests

def fetch_customer_profile(request):
    api_url = f'{settings.API_BASE_URL}profile/'
    response = requests.get(
        api_url,
        headers={
            'Authorization': f"Bearer {request.COOKIES.get('access_token')}"
        }, proxies={"http": None, "https": None}
    )
    if response.status_code == 200:
        return response.json()
    return None
