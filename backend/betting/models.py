from django.db import models
from django.contrib.auth.models import User
from catalog.models import Driver, Race


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BetStat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='betstats')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='betstats')
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class Bet(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='bets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='bets')
    bet_date = models.DateTimeField(auto_now_add=True)
    bet_top_3 = models.ManyToManyField(Driver, related_name='bet_top_3', blank=True)
    bet_last_5 = models.ForeignKey(Driver, related_name='bet_last_5', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    bet_last_10 = models.ForeignKey(Driver, related_name='bet_last_10', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    bet_fastest_lap = models.ForeignKey(
        Driver,
        related_name='fastest_lap_bets_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)


class Meta:
    unique_together = (('user', 'race'),)
