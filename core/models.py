from django.db import models


class SiteInfo(models.Model):
    site_name = models.CharField(max_length=255)
    site_number = models.CharField(max_length=15)
    site_email = models.EmailField()
    site_description = models.TextField()
    site_slogan = models.CharField(max_length=255)
    copyright_text = models.TextField()

    youtube_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)

    def __str__(self):
        return self.site_name


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True