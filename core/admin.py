from django.contrib import admin
from .models import SiteInfo

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_email', 'site_number')
    fieldsets = (
        ('اطلاعات عمومی', {
            'fields': ('site_name', 'site_slogan', 'site_description', 'copyright_text')
        }),
        ('اطلاعات تماس', {
            'fields': ('site_number', 'site_email')
        }),
        ('لینک‌های اجتماعی', {
            'fields': ('youtube_link', 'twitter_link', 'instagram_link', 'telegram_link', 'linkedin_link')
        }),
        ('لوگو و فاوآیکون', {
            'fields': ('logo', 'favicon')
        }),
    )  
