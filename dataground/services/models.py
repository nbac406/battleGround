from django.db import models

class players(models.Model):
    account_id = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    shard_id = models.CharField(max_length=100)
    match_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        unique_together = [('account_id', 'match_id')]

class match_summarys(models.Model):
    players_table = models.ForeignKey(players, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=200, unique=True)
    game_mode = models.CharField(max_length=20)
    map_name = models.CharField(max_length=30)
    duration = models.IntegerField()
    match_type = models.CharField(max_length=20)
    asset_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=False)

class weapon_masterys(models.Model):
    players_table = models.ForeignKey(players, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=100, unique=True)
    first_weapon_name = models.CharField(max_length=100)
    first_weapon_XPtotal = models.IntegerField()
    second_weapon_name = models.CharField(max_length=100)
    second_weapon_XPtotal = models.IntegerField()
    third_weapon_name = models.CharField(max_length=100)
    third_weapon_XPtotal = models.IntegerField()
    weapon_cluster = models.CharField(max_length=20)

class match_participants(models.Model):
    players_table = models.ForeignKey(players, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=200)
    player_name = models.CharField(max_length=100)
    account_id = models.CharField(max_length=200)
    roster_id = models.CharField(max_length=200)
    team_ranking = models.IntegerField()
    dbnos = models.IntegerField()
    assists = models.IntegerField()
    damage_dealt = models.FloatField()
    headshot_kills = models.IntegerField()
    kills = models.IntegerField()
    longest_kill = models.IntegerField()
    team_kills = models.IntegerField()
    ride_distance = models.FloatField()
    swim_distance = models.FloatField()
    walk_distance = models.FloatField()

    def __str__(self):
        return f"{self.match_id}, {self.player_name}, {self.account_id}, {self.roster_id}, {self.team_ranking}, {self.dbnos}, {self.assists}, {self.damage_dealt}, {self.headshot_kills}, {self.kills}, {self.longest_kill}, {self.team_kills}, {self.ride_distance}, {self.walk_distance}, {self.swim_distance}"
    
    class Meta:
        unique_together = [('account_id', 'match_id')]

class position_logs(models.Model):
    players_table = models.ForeignKey(players, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=200)
    player_name = models.CharField(max_length=100)
    account_id = models.CharField(max_length=200)
    location_x = models.FloatField()
    location_y = models.FloatField()
    event_time = models.IntegerField()

    class Meta:
        unique_together = [('account_id', 'match_id', 'event_time')]

class kill_logs(models.Model):
    players_table = models.ForeignKey(players, on_delete=models.CASCADE)
    match_id = models.CharField(max_length=200)
    victim_name = models.CharField(max_length=100)
    killer_name = models.CharField(max_length=100)
    victim_account_id = models.CharField(max_length=200)
    killer_account_id = models.CharField(max_length=200)
    victim_x = models.FloatField()
    victim_y = models.FloatField()
    killer_x = models.FloatField()
    killer_y = models.FloatField()
    event_time = models.IntegerField()

    class Meta:
        unique_together = [('match_id', 'victim_account_id', 'killer_account_id')]

class weapons(models.Model):
    weapon_name = models.CharField(max_length=100, unique=True)
    weapon_type = models.CharField(max_length=20)
    weapon_tier = models.IntegerField()
    first_easy_weapon = models.CharField(max_length=30)
    first_easy_percent = models.FloatField()
    second_easy_weapon = models.CharField(max_length=30)
    second_easy_percent = models.FloatField()
    third_easy_weapon = models.CharField(max_length=30)
    third_easy_percent = models.FloatField()
    first_hard_weapon = models.CharField(max_length=30)
    first_hard_percent = models.FloatField()
    second_hard_weapon = models.CharField(max_length=30)
    second_hard_percent = models.FloatField()
    third_hard_weapon = models.CharField(max_length=30)
    third_hard_percent = models.FloatField()
    graph_image_url = models.CharField(max_length=1000)

class weapon_parts(models.Model):
    weapons_table = models.ForeignKey(weapons, on_delete=models.CASCADE)
    weapon_name = models.CharField(max_length=100)
    parts_name = models.CharField(max_length=100)
    parts_type = models.CharField(max_length=50)
    utilization_rate = models.FloatField()

class maps(models.Model):
    map_name = models.CharField(max_length=20)
    start_point  = models.IntegerField()
    end_point = models.IntegerField()
    image_url = models.CharField(max_length=1000)

    class Meta:
        unique_together = [('map_name', 'start_point', 'end_point')]