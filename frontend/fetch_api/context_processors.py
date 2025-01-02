import requests
from django.conf import settings
from fetch_api.request_view.utils import fetch_customer_profile


def site_info(request):
    api_url = f"{settings.API_BASE_URL}site-info"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            site_info = data.get("results", [])[0] if data.get("results") else {}
            return {"site_info": site_info}
        else:
            return {"site_info": None, "error": "Failed to fetch data from API"}

    except requests.exceptions.RequestException as e:
        return {"site_info": None, "error": f"An error occurred: {str(e)}"}


def categories(request):
    api_url = f"{settings.API_BASE_URL}categories/"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            categories = data.get("results", [])
            return {"category_list": categories}
        else:
            return {"category_list": []}

    except requests.exceptions.RequestException as e:
        return {"category_list": [], "error": f"An error occurred: {str(e)}"}
    

def user_profile_context(request):
    profile_data = fetch_customer_profile(request)
    if profile_data:
        first_name = profile_data.get('first_name', 'کاربر')
        last_name = profile_data.get('last_name', '')
        email = profile_data.get('email', '')
    else:
        first_name = 'کاربر'
        last_name = ''
        email = ''

    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }