from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Owner(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

class FoodItem(models.Model):
    name = models.CharField(max_length=60)
    doordash_price = models.DecimalField(max_digits = 5, decimal_places=2, default=0.0)
    uber_price = models.DecimalField(max_digits = 5, decimal_places=2, default=0.0)
    image_name = models.CharField(max_length=30,default='')
    type = models.CharField(max_length=30)
    likes = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name='likers', blank=True)

    def __str__(self) -> str:
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    cuisine = models.CharField(max_length=20) #food type
    price_range = models.CharField(max_length=7)
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE)
    uber_delivery_time = models.CharField(max_length=10, default='0 Mins')
    doordash_delivery_time = models.CharField(max_length=10, default='0 Mins')
    image_name = models.CharField(max_length=255,default='')
    banner_name = models.CharField(max_length=255,default='')
    uberlink = models.CharField(max_length=255, default='')
    doordashlink = models.CharField(max_length=255, default='')
    favorites = models.IntegerField(default=0)
    favoriters = models.ManyToManyField(User, related_name='favoriters', blank=True)


    def __str__(self) -> str:
        return self.name

class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    food_items = models.ManyToManyField(FoodItem)

    def __str__(self) -> str:
        return self.restaurant.name + " Menu"

def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError(_('Rating must be between 1 and 5'))

class Reviews(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])
    review = models.TextField(default='',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("reviewer", "restaurant"),)

    def __str__(self) -> str:
        return self.reviewer.username + ": " + self.restaurant.name + " - " + str(self.rating)

class Deals(models.Model):
    name = models.CharField(max_length=256)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=256)
    code = models.CharField(max_length=256, default= '')
    def __str__(self) -> str:
        return self.restaurant.name + " : " + self.name