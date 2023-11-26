from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Image
from .exception import Deupicated


# @receiver(pre_save, sender=Image)
# def duplicated_image(sender, instance, *args, **kwargs):
#     if instance.filter().exists():
#         raise Deupicated('Duplicated image')
#     return instance