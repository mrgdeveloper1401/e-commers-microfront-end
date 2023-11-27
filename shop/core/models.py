from typing import Any
from django.db import models
from django.conf import settings
from django.utils import timezone



class AuditableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created', blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='modified', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)


# class SoftDelete(models.Model):
#     is_deleted = models.BooleanField(default=False, editable=False)
#     deleted_at = models.DateTimeField(editable=False, blank=True, null=True)
    
#     def delete(self, using, keep_parent):
#         self.is_deleted = True
#         self.deleted_at = timezone.now()
#         self.save()
#         return super().delete()
    
#     class QuerySet(models.QuerySet):
#         pass
    
    
    class Meta:
        abstract = True