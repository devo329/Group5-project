from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    doordash_price = models.DecimalField(max_digits = 5, decimal_places=2, default=0.0)
    uber_price = models.DecimalField(max_digits = 5, decimal_places=2, default=0.0)

    def __str__(self) -> str:
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    cuisine = models.CharField(max_length=20) #food type
    price_range = models.CharField(max_length=7)
    owner = models.OneToOneField(Owner, null=True, on_delete=models.CASCADE, primary_key=False)
    uber_delivery_time = models.CharField(max_length=10, default='0 Mins')
    doordash_delivery_time = models.CharField(max_length=10, default='0 Mins')
    image_name = models.CharField(max_length=30,default='')


    def __str__(self) -> str:
        return self.name

class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    food_items = models.ManyToManyField(FoodItem)

    def __str__(self) -> str:
        return self.restaurant.name + " Menu"


class Reviews(models.Model):
    Reviewer = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)
    rating = models.IntegerField(default=0)
    review = models.TextField(default='')

    def __str__(self) -> str:
        return self.Reviewer.username + " - " + str(self.rating)

class Ratings(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True, default= '')
    reviews = models.ManyToManyField(Reviews)

