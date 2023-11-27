from django.db import models
from django.conf import settings



class AuditableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created', blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)


class SoftDelete(models.Model):
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='deleted_by',)
    deleted_at = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True