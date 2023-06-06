from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""Креирајте Djangо апликација за менаџирање на работилница за поправка на 
автомобили. 
Секоја закажана поправка се карактеризира со задолжителен код, датум кога е 
пријавена поправката, опис на проблемот за поправање, корисник кој ја пријавил 
поправката, фотографија од проблемот, информација за автомобилот што треба да се 
поправи и работилница која е избрана да ја направи поправката. 



За работилницата се чуваат нејзиното име, година на 
основање и информација дали поправа стари (oldtimer) возила. 

За секој производител на 
автомобили се чува информација за името на производителот, линк до официјалната страна, 
земја на потекло и име на сопственикот.

Дополнително, за секоја работилница се чува информација за производителите на 
автомобили за чии автомобили е специјализирана да ги поправа. Еден производител може 
да соработува со повеќе работилници."""


class WorkShop(models.Model):
    name = models.CharField(max_length=50)
    year_founded = models.PositiveIntegerField()
    repairs_oldtimers = models.BooleanField()

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50)
    url = models.URLField()
    owner_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    type = models.CharField(max_length=50)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    max_speed = models.PositiveIntegerField()
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Repair(models.Model):
    code = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class ProducerWorkshop(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producer} - {self.workshop}"
