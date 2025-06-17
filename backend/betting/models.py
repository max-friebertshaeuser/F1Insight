import uuid

from django.db import models
from django.contrib.auth.models import User
from catalog.models import Driver, Race


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    join_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

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
    bet_last_5 = models.ForeignKey(Driver, related_name='bet_last_5', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    bet_last_10 = models.ForeignKey(Driver, related_name='bet_last_10', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    bet_fastest_lap = models.ForeignKey(Driver, related_name='fastest_lap_bets', on_delete=models.SET_NULL,
                                        null=True, blank=True)

    evaluated = models.BooleanField(
        default=False,
    )

    bet_top_3 = models.ManyToManyField(
        Driver,
        through='BetTop3',
        related_name='bets_top3'
    )


class BetTop3(models.Model):
    bet       = models.ForeignKey(Bet, on_delete=models.CASCADE)
    driver    = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position  = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['position']
        unique_together = [['bet', 'position']]

class Meta:
    unique_together = (('user', 'race'),)
