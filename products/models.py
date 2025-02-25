from django.db import models


class Product(models.Model):
    """A class to represent a set of products."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.CharField(max_length=2083)

    def __str__(self):
        return self.name


class Offer(models.Model):
    """A class to represent the available offers."""
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()

