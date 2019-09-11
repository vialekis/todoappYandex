# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    api_key = models.CharField("Trello key",max_length=64, blank=True, null=True)
    api_secret = models.CharField("Trello token",max_length=64, blank=True, null=True)

    def __str__(self):
        return "Профиль пользователя %s" % self.user.username