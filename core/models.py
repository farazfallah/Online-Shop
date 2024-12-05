from django.db import models
from django.utils.timezone import now


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


class LogicalDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(updated_at__isnull=False)

    def deleted(self):
        return super().get_queryset().filter(updated_at__isnull=True)

    def all_with_deleted(self):
        return super().get_queryset()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LogicalDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.updated_at = None
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
