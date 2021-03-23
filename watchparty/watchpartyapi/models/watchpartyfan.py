from django.db import models


class WatchPartyFan(models.Model):
    watchparty = models.ForeignKey("WatchParty", on_delete=models.CASCADE)
    fan = models.ForeignKey("Fan", on_delete=models.CASCADE)
