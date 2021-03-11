from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=55)
    sport_type = models.ForeignKey("SportType", on_delete=models.CASCADE)
    team_one = models.CharField(max_length=50)
    team_two = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=250)
