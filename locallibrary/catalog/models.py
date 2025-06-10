from django.db import models

# Create your models here.
from django.db import models
import uuid

class Season(models.Model):
    season_id = models.CharField(primary_key=True, max_length=10)

class Circuit(models.Model):
    circuit_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=10)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)

class Constructor(models.Model):
    constructor_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

class Race(models.Model):
    race_id = models.CharField(primary_key=True, max_length=10)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    round = models.IntegerField()
    date = models.DateField()

class DriverTeam(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('season', 'driver'),)

class QualifyingResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()
    q1 = models.TimeField(null=True, blank=True)
    q2 = models.TimeField(null=True, blank=True)
    q3 = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = (('race', 'driver'),)

class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    grid = models.IntegerField()
    position = models.IntegerField()
    position_text = models.TextField()
    points = models.FloatField()
    laps = models.IntegerField()
    time = models.TextField()
    status = models.TextField()

    class Meta:
        unique_together = (('race', 'driver'),)

class LapTime(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    lap = models.IntegerField()
    position = models.IntegerField()
    time = models.TextField()
    milliseconds = models.IntegerField()

    class Meta:
        unique_together = (('race', 'driver', 'lap'),)

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

class Bet(models.Model):
    bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10)  # pending, won, lost
