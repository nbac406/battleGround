from django.db import models

class players(models.Model):
    accountId = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    shardid = models.CharField(max_length=100)
    matchId = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        unique_together = [('accountId', 'matchId')]

class match_summary(models.Model):
    matchId = models.CharField(max_length=200)
    gamemode = models.CharField(max_length=20)
    mapname = models.CharField(max_length=30)
    duration = models.IntegerField()
    match_type = models.CharField(max_length=20)
    asset_url = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=False)

class weapon_mastery(models.Model):
    accountId = models.CharField(max_length=100)
    Item_Weapon_name = models.CharField(max_length=100)
    Item_Weapon_XPtotal = models.IntegerField()

class match_participant(models.Model):
    matchId = models.CharField(max_length=200)
    player_name = models.CharField(max_length=100)
    accountId = models.CharField(max_length=200)
    rosterId = models.CharField(max_length=200)
    team_ranking = models.IntegerField()
    dbnos = models.IntegerField()
    assists = models.IntegerField()
    damage_dealt = models.FloatField()
    headshot_kills = models.IntegerField()
    kills = models.IntegerField()
    longestkill = models.IntegerField()
    team_kills = models.IntegerField()
    ride_distance = models.FloatField()
    swim_distance = models.FloatField()
    walk_distance = models.FloatField()

    class Meta:
        unique_together = [('accountId', 'matchId')]

class logs(models.Model):
    asset_url = models.ForeignKey(match_summary, on_delete=models.CASCADE)
    matchId = models.CharField(max_length=200)
    player_name = models.CharField(max_length=100)
    accountId = models.CharField(max_length=200)
    team_id = models.IntegerField()
    victim = models.CharField(max_length=100)
    killer = models.CharField(max_length=100)
    location_x = models.FloatField()
    location_y = models.FloatField()
    location_z = models.FloatField()
    _D = models.DateTimeField(auto_now_add=False)

class weapons(models.Model):
    weapon_name = models.CharField(max_length=100)
    weapon_type = models.CharField(max_length=20)

class weapon_parts(models.Model):
    parts_name = models.CharField(max_length=100)
    parts_type = models.CharField(max_length=50)

class maps(models.Model):
    map_name = models.CharField(max_length=20)
