from django.db import models


class WatchParty(models.Model):
    name = models.CharField(max_length=50)
    scheduled_time = models.TimeField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    number_of_fans = models.IntegerField()
