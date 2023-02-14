from django.shortcuts import render
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Avg, Count, Sum
from .forms import ReviewForm


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


def loading_screen(request):
    return render(request, 'loading.html')


def index(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    context = {'restaurant_rating_data': restaurant_rating_data}
    return render(request, "index.html", context)


def restaurant(request):
    id = request.GET.get('id')
    menu = FoodItem.objects.filter(menu__restaurant__name=id)
    featured = FoodItem.objects.filter(
        menu__restaurant__name=id).order_by('-likes')[:3]
    info = Restaurant.objects.filter(name=id)
    rating = getRating(id)
    num_reviews, reviews, count, distributed_list = getReviews(id)
    categories = getAndFormatCategories(id)

    context = {'menu': menu,
               'restaurant': info,
               'featured': featured,
               'categories': categories,
               'rating': rating,
               'reviews': reviews,
               'num': num_reviews,
               'count': count,
               'distributions': distributed_list,
               'name': id,
               }
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

def error(request):
    return render(request, 'error.html')

@login_required
def addReview(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        id = request.POST.get('restaurant')
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = Restaurant.objects.filter(name = request.POST.get('restaurant'))[:1].get()
            review.reviewer = User.objects.filter(username = request.POST.get('reviewer'))[:1].get()
            review.rating = int(request.POST.get('rating'))
            review.review = request.POST.get('review')
            review.save()

            return redirect(reverse('restaurant') + "?id=" + id)
        else:
            return redirect(reverse('error'))
    else:
        print('error')
        form = ReviewForm()

    return redirect(reverse('restaurant') + "?id=McDonalds")
