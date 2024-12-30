import fetch_api
from django.views.generic import TemplateView

class SiteInfoView(TemplateView):
    template_name = "base.html"  # نام قالب شما

    def get_context_data(self, **kwargs):
        # فراخوانی کانتکست پیش‌فرض
        context = super().get_context_data(**kwargs)

        # URL API
        api_url = "http://127.0.0.1:8000/api/site-info"

        try:
            # ارسال درخواست GET به API
            response = fetch_api.get(api_url)

            # اگر پاسخ موفق بود
            if response.status_code == 200:
                data = response.json()  # تبدیل پاسخ به JSON
                
                # فقط اولین نتیجه را برگردانید
                site_info = data.get("results", [])[0] if data.get("results") else {}
                
                # افزودن داده‌ها به کانتکست
                context["site_info"] = site_info
            else:
                # اگر API پاسخ موفق نداد، پیام خطا اضافه کنید
                context["error"] = "Failed to fetch data from API"

        except fetch_api.exceptions.RequestException as e:
            # مدیریت خطای درخواست
            context["error"] = f"An error occurred: {str(e)}"

        return context
