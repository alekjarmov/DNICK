from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Balloon(models.Model):
    type = models.CharField(max_length=50)
    producer_name = models.CharField(max_length=50)
    max_passengers = models.IntegerField()


class Pilot(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_birth = models.IntegerField()
    time_flied = models.IntegerField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + self.last_name


class Company(models.Model):
    name = models.CharField(max_length=50)
    year_founded = models.IntegerField()
    flies_outside_europe = models.BooleanField()
    pilots = models.ManyToManyField(Pilot, "pilots")


class Flight(models.Model):
    code = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    airport_from = models.CharField(max_length=50)
    airport_to = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="images/", null=True, blank=True)
    pilot = models.ForeignKey(Pilot, related_name="pilot", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
