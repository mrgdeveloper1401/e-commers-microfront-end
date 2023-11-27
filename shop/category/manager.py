from django.db import models


class CategortPublisher(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_publish=True)