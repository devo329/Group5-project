from django.shortcuts import render

import restaurants
#from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from django.db.models import Avg
from django.shortcuts import render

def getRatings(restaurants):
    restaurant_rating_data = []
    for restaurant in restaurants:
        ratings = restaurant.reviews_set.all().aggregate(Avg('rating'))
        avg_rating = ratings['rating__avg']
        restaurant_rating_data.append({'restaurant': restaurant, 'avg_rating': avg_rating})

    return restaurant_rating_data

def index(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    context = {'restaurant_rating_data': restaurant_rating_data}
    return render(request, "index.html", context)

def restaurant(request):
    id = request.GET.get('id')
    menu = FoodItem.objects.filter(menu__restaurant__name = id)
    info = Restaurant.objects.filter(name = id)
    context = {'menu' : menu,'restaurant': info}
    return render(request, "restaurant.html", context)