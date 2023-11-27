from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel


class User(AbstractUser, SoftDeleteModel):
    email = models.EmailField(unique=True, blank=True)
    mobile_phone = models.CharField(max_length=11, unique=True, db_index=True)
    REQUIRED_FIELDS = ('email', 'mobile_phone')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, editable=False)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True, editable=False)
    verify_email = models.BooleanField(default=False)
    verify_mobile_phone = models.BooleanField(default=False)
    update_user = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = 'User'
        

class UserProxy(User):
    class Meta:
        proxy = True