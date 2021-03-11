from django.db import models


class WatchPartyFan(models.Model):
    watch_party = models.ForeignKey("WatchParty", on_delete=models.CASCADE)
    fan = models.ForeignKey("Fan", on_delete=models.CASCADE)
