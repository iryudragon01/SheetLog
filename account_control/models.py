from django.db import models
from django.utils import timezone


# Create your models here.
class UserStart(models.Model):
    username = models.CharField(max_length=200)
    user_superior = models.PositiveIntegerField(default=99)  # 1 is highest 99 is lowest
    date_log = models.DateTimeField()
    version_log = models.PositiveIntegerField(default=0)
    last_login = models.DateTimeField(default=timezone.now())

