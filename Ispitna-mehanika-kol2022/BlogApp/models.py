from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""
Задача: Креирајте Djangо апликација за менаџирање на продавница за здрава храна. Секој 
прехранбен продукт се карактеризира со автоматски генерирана шифра, име, опис и
информација за тоа во која категорија припаѓа, корисникот кој го креирал продуктот, 
фотографија од продуктот, цена и количина. За секоја категорија се чува име, опис и дали е 
активна (bool). За секоја продажба во системот се евидентираат продуктите кои биле 
продадени (секој со соодветна количина), датумот на продажба и клиентот кој ги купил. За 
секој клиент се чува име, презиме, адреса и емаил.
"""


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField()

    def __str__(self):

        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"


class Sale(models.Model):
    date = models.DateField()
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.buyer} at {self.date}")


class ProductSale(models.Model):
    product = models.ForeignKey(Client, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return (f"{self.sale}-{self.product}: {self.quantity}")

