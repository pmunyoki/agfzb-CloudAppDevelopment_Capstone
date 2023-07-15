from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=200, default="name")
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f'Car make is {self.name}'

class CarModel(models.Model):
    CAR_TYPES = [
        ("SEDAN", 'Sedan'),
        ("SUV", 'suv'),
        ("WAGON", 'Wagon')
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="name")
    dealer_id = models.IntegerField(default=0)
    type = models.CharField(max_length=5, choices=CAR_TYPES, default="Sedan")
    year = models.DateField(null=True)

    def __str__(self):
        return f'Car make is {self.car_make}, the model is {self.name}'

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

