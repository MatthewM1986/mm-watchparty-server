from django.db import models


class SportType(models.Model):
    type = models.CharField(max_length=50)
