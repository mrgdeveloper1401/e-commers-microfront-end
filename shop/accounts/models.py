from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    mobile_phone = models.CharField(max_length=11, unique=True, db_index=True)
    REQUIRED_FIELDS = ('email', 'mobile_phone')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, editable=False)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True, editable=False)

    class Meta:
        db_table = 'User'