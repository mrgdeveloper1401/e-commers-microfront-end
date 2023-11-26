from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    mobile_phone = models.CharField(max_length=11, unique=True, db_index=True)
    REQUIRED_FIELDS = ('email', 'mobile_phone')
 