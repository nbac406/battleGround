from django.db import models

class player(models.Model):
    accountId = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    shardid = models.CharField(max_length=100)
    matchId = models.JSONField()
