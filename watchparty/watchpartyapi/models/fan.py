from django.db import models
from django.contrib.auth.models import User


class Fan(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fav_sport = models.CharField(max_length=50)
    fav_team = models.CharField(max_length=50)
