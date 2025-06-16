from django.db import models
from django.contrib.auth.models import User
from catalog.models import Driver, Race


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='betting_groups')

class BetStat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = (models.IntegerField(default=0))

class Bet(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    bet_date = models.DateTimeField(auto_now_add=True)
    bet_top_3 = models.JSONField(default=list)
    bet_last_5 = models.JSONField(default=list)
    bet_last_10 = models.JSONField(default=list)
    bet_fastest_lap = models.ForeignKey(Driver, related_name='fastest_lap_bets', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        unique_together = (('user', 'race'),)
