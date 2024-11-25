from django.db import models
from django.utils.timezone import now

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
