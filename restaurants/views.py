from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Avg

import restaurants

from django.template import Library

register = Library()

def getAndFormatCategories(restaurant):
    categories = FoodItem.objects.filter(menu__restaurant__name = restaurant).distinct().values_list('type', flat=True).order_by('type')
    category_list = []
    for item in categories:
        category_list.append(item)

    if category_list.__contains__('Dessert'):
        category_list.append(category_list.pop(category_list.index('Dessert')))

    if category_list.__contains__('Drink'):
      category_list.append(category_list.pop(category_list.index('Drink')))

    return category_list

# Create your views here.
def getRatings(restaurants):
    restaurant_rating_data = []
    for restaurant in restaurants:
        ratings = restaurant.reviews_set.all().aggregate(Avg('rating'))
        avg_rating = ratings['rating__avg']
        if isinstance(avg_rating, float):
            avg_rating = int(avg_rating)
            restaurant_rating_data.append({'restaurant': restaurant, 'avg_rating': avg_rating})
        else:
            restaurant_rating_data.append({'restaurant': restaurant, 'avg_rating': avg_rating})

    return restaurant_rating_data

def loading_screen(request):
    return render(request, 'loading.html')

def index(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    context = {'restaurant_rating_data': restaurant_rating_data}
    return render(request, "index.html", context)

def restaurant(request):
    id = request.GET.get('id')
    menu = FoodItem.objects.filter(menu__restaurant__name = id)
    featured = FoodItem.objects.filter(menu__restaurant__name = id).order_by('-likes')[:3]
    info = Restaurant.objects.filter(name = id)
    avg_rating = Reviews.objects.filter(restaurant__name=id).aggregate(Avg('rating'))
    rating = avg_rating['rating__avg']
    if isinstance(rating, float):
        rating = int(rating)
    else:
        rating = rating

    category_list = getAndFormatCategories(id)
    print(category_list)
    context = {'menu' : menu,'restaurant': info, 'featured' : featured, 'categories' : category_list, 'rating' : rating}
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
