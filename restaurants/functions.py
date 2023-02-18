from restaurants.models import *
from .models import *
from django.db.models import Avg, Count
from .forms import *
from .functions import *

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


def getReviews(id):
    reviews = Reviews.objects.filter(restaurant__name=id).all()
    reviews_count = Reviews.objects.filter(restaurant__name=id).values(
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