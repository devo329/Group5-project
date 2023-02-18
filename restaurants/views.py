from django.shortcuts import render
from .forms import NewUserForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from .functions import *
from django.contrib import messages
from django.contrib.auth import login, logout


def loading_screen(request):
    return render(request, 'loading.html')


def index(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owners = Owner.objects.all()
    owners_list = []
    for owner in owners:
        owners_list.append(owner.user)

    context = {'restaurant_rating_data': restaurant_rating_data, 'owners' : owners}
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

@login_required
def favorite(request,restaurant_id):
    restaurant = Restaurant.objects.get(name = restaurant_id)

    if request.user not in restaurant.favoriters.all():
        restaurant.favorites += 1
        restaurant.favoriters.add(request.user)
        restaurant.save()

    elif request.user in restaurant.favoriters.all():
        restaurant.favorites -= 1
        restaurant.favoriters.remove(request.user)
        restaurant.save()

    return redirect(reverse('restaurant') + "?id=" + restaurant_id)

def error(request):
    return render(request, 'error.html')

def owner_dashboard(request):
    return render(request, 'owner-dashboard.html')

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

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("index")

def create_restaurant(request):
    id = request.GET.get('id')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RestaurantForm()
        restaurant = Restaurant.objects.filter(owner_id= id)
        owner_info = Owner.objects.filter(id= id)[0]
        restaurants = Restaurant.objects.all()
        restaurant_rating_data = getRatings(restaurants)
        context = {
            'form':form,
            'owner_info': owner_info,
            'restaurant_rating_data': restaurant_rating_data,
        }

    return render(request, 'owner-dashboard.html', context)