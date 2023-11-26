from django.db import models
from django.contrib.admin.models import LogEntry



class FoorPrint(models.Model):
    pass


class LogEntries(LogEntry):
    pass


class ActionHistory(LogEntry):
    class Meta:
        proxy = True

