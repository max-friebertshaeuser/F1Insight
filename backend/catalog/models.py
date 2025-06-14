from django.db import models

# Create your models here.
from django.db import models
import uuid

class DataUpdate(models.Model):
    name      = models.CharField(max_length=50, unique=True)
    last_run  = models.DateTimeField(auto_now=True)

class Season(models.Model):
    season = models.CharField(primary_key=True, max_length=5)

class Circuit(models.Model):
    circuit = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Driver(models.Model):
    driver = models.CharField(primary_key=True, max_length=100)
    number = models.CharField(max_length=100, blank=True)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)

class Constructor(models.Model):
    constructor = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

class Race(models.Model):
    date = models.DateField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    round = models.CharField(max_length=100)

class DriverTeam(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    driver_season_number = models.CharField(max_length=100)

    class Meta:
        unique_together = (('season', 'driver'),)

class QualifyingResult(models.Model):
    date = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    q1 = models.CharField(null=True, blank=True, max_length=100)
    q2 = models.CharField(null=True, blank=True, max_length=100)
    q3 = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        unique_together = (('date', 'driver'),)

class Result(models.Model):
    date = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    grid = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    position_text = models.CharField(max_length=100)
    points = models.CharField(max_length=100)
    laps = models.CharField(max_length=100)
    time = models.CharField(max_length=100, blank=True)
    fastest_lap = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100)

    class Meta:
        unique_together = (('date', 'driver'),)

# class LapTime(models.Model):
#     date = models.ForeignKey(Race, on_delete=models.CASCADE)
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     lap = models.CharField(max_length=100)
#     position = models.CharField(max_length=100)
#     time = models.CharField(max_length=100)
#     milliseconds = models.IntegerField()
#
#     class Meta:
#         unique_together = (('date', 'driver', 'lap'),)

class Driverstanding(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    positionText = models.CharField(max_length=100)
    points = models.CharField(max_length=100)
    wins = models.CharField(max_length=100)

    class Meta:
        unique_together = (('season', 'driver'),)


class Constructorstanding(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    positionText = models.CharField(max_length=100)
    points = models.CharField(max_length=100)
    wins = models.CharField(max_length=100)

    class Meta:
        unique_together = (('season', 'constructor'),)


class User(models.Model):
    user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

class Bet(models.Model):
    bet = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10)  # pending, won, lost
