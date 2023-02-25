from restaurants.models import *
from .models import *
from django.db.models import Avg, Count
from .forms import *
from .functions import *
import re

def getAndFormatCategories(restaurant):
    categories = FoodItem.objects.filter(menu__restaurant__name=restaurant).distinct(
    ).values_list('type', flat=True).order_by('type')
    category_list = []
    for item in categories:
        category_list.append(item)

    if category_list.__contains__('Desserts'):
        category_list.append(category_list.pop(
            category_list.index('Desserts')))

    if category_list.__contains__('Drinks'):
        category_list.append(category_list.pop(category_list.index('Drinks')))

    return category_list

# Create your views here.


def getRatings(restaurants):
    restaurant_rating_data = []
    for restaurant in restaurants:
        ratings = restaurant.reviews_set.all().aggregate(Avg('rating'))
        avg_rating = ratings['rating__avg']
        if isinstance(avg_rating, float):
            avg_rating = int(avg_rating)
            restaurant_rating_data.append(
                {'restaurant': restaurant, 'avg_rating': avg_rating})
        else:
            restaurant_rating_data.append(
                {'restaurant': restaurant, 'avg_rating': avg_rating})

    return restaurant_rating_data


def getRating(id):
    avg_rating = Reviews.objects.filter(
        restaurant__name=id).aggregate(Avg('rating'))
    rating = avg_rating['rating__avg']
    if isinstance(rating, float):
        rating = int(rating)
    else:
        rating = rating

    return rating


def getReviews(id,type):
    if type == 'restaurant':
        reviews = Reviews.objects.filter(restaurant__name=id).all()
        reviews_count = Reviews.objects.filter(restaurant__name=id).values(
        'rating').annotate(c=Count('rating')).order_by('rating')
    else:
        reviews = Reviews.objects.filter(reviewer=id).all()
        reviews_count = Reviews.objects.filter(reviewer=id).values(
        'rating').annotate(c=Count('rating')).order_by('rating')

    toReturn = []
    for r in reviews_count:
        toReturn.append({r['rating']: r['c']})

    num_reviews = len(reviews)
    expected_keys = {1, 2, 3, 4, 5}
    present_keys = set()
    for item in toReturn:
        present_keys.update(item.keys())

    missing_keys = expected_keys - present_keys

    for i in missing_keys:
        toReturn.append({i: 0})

    sorted_list = sorted(toReturn, key=lambda x: list(x.keys())[0])

    key_values = [d.values() for d in sorted_list]

    flat_list = [value for values in key_values for value in values]

    distributed_list = []

    if num_reviews != 0:
        for i in range(0, 5):
            distributed_list.append(
                {'rating': i + 1, 'distribution': int((flat_list[i]/num_reviews)*100)})

    return (num_reviews, reviews, sorted_list, distributed_list)

def getNumLikes(id):
    menus = Menu.objects.filter(restaurant__owner = id)
    food_items_list = []
    for m in menus:
        food_items_list = FoodItem.objects.filter(menu = m)

    likes = 0
    for item in food_items_list:
        likes = likes + item.likes

    return likes

def getNumFavorited(id):
    restaurants = Restaurant.objects.filter(owner__id=id).all()
    favorites = 0
    for restaurant in restaurants:
        favorites = favorites + restaurant.favorites

    return favorites

def avgRatings(id):
    restaurants = Restaurant.objects.filter(owner_id= id)
    sum = 0
    count = 0
    for restaurant in restaurants:
        rating = getRating(restaurant.name)
        if rating is not None:
            sum = sum + rating
            count = count + 1

    if count != 0:
        return int(sum/count)
    else:
        return None

def getMenu(id):
    restaurant = Restaurant.objects.filter(owner_id= id)
    list = []
    for r in restaurant:
        menu = FoodItem.objects.filter(menu__restaurant__name=r.name)
        list.append({'name': r.name, 'menu': menu})
    return list

def parse_mins(id):
    info = Restaurant.objects.get(name=id)
    uber_time = info.uber_delivery_time
    doordash_time = info.doordash_delivery_time

    match = re.search(r'^(\d+)', uber_time)
    if match:
        uber_time = int(match.group(1))

    match = re.search(r'^(\d+)', doordash_time)
    if match:
        doordash_time = int(match.group(1))

    return(uber_time,doordash_time)

def getCompetition(all_restaurants,restaurants):
    all_cuisines = set()
    owner_cuisines = set()
    all_restaurantsSet = set()
    restaurantsSet = set()
    for a in all_restaurants:
        all_restaurantsSet.add(a)
        all_cuisines.add(a.cuisine)

    for a in restaurants:
        restaurantsSet.add(a)
        owner_cuisines.add(a.cuisine)

    cuisines = all_cuisines.intersection(owner_cuisines)
    not_owned = all_restaurantsSet.difference(restaurantsSet)

    toReturn = []
    for c in not_owned:
        if c.cuisine in cuisines:
            toReturn.append(c)

    return toReturn