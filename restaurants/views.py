from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Avg

import restaurants

# Create your views here.
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

@login_required
def like(request, item_id, restaurant_id):
    item = FoodItem.objects.get(id=item_id)

    if request.user not in item.likers.all():
        item.likes += 1
        item.likers.add(request.user)
        item.save()

    elif request.user in item.likers.all():
        item.likes -= 1
        item.likers.remove(request.user)
        item.save()

    return redirect(reverse('restaurant') + "?id=" + restaurant_id)








