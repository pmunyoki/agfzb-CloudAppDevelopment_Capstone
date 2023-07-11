from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = name = models.CharField(max_length=200, default="name")
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
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


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

