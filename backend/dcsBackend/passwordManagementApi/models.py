from django.db import models

# Create your models here.

from django.db import models
from usrManApi.models import CustomUser


class UserReset(models.Model):
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=200, null=True, blank=True)
    @property
    def user_email(self):
        return self.user.email
    def __str__(self):
        return self.email
