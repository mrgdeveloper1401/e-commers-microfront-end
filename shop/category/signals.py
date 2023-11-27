from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Category
from django.conf.global_settings import AUTH_USER_MODEL


# @receiver(post_save, sender=Category)
# def set_user(sender, instance, created, **kwargs):
#     if created:
#         instance.created_by = instance.created_by
#         instance.save()
