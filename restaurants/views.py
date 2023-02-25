from django.shortcuts import render
from .forms import NewUserForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from .functions import *
from django.contrib import messages
from django.contrib.auth import login, logout



@login_required
def clip_deal(request, deal_id):
    if request.method == 'POST':
        deal = Deals.objects.get(id=deal_id)

    if request.user not in deal.clippers.all():
        deal.clipped += 1
        deal.clippers.add(request.user)
        deal.save()

    return redirect(reverse('deals'))

def deals(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    deals = Deals.objects.all()
    context = {'restaurant_rating_data': restaurant_rating_data, 'owner': owner, 'deals' : deals}
    return render(request, "deals.html", context)


def loading_screen(request):
    return render(request, 'loading.html')

@login_required
def user_dashboard(request):
    id = request.GET.get('id')
    user = get_object_or_404(User, id=id)

    if request.user != user:
        return redirect('index')

    favorited = Restaurant.objects.filter(favoriters = user)
    clipped = Deals.objects.filter(clippers = user)
    liked = FoodItem.objects.filter(likers = user)
    reviews = Reviews.objects.filter(reviewer = user)
    null, null, count, distributed_list = getReviews(user,'user')
    sum = 0
    count = 0
    for r in reviews:
        sum = sum + r.rating
        count = count + 1

    if count == 0:
        rating = 0
    else:
        rating = sum/count

    context = {
        'favorited' : favorited,
        'clipped' : clipped,
        'liked' : liked,
        'reviews' : reviews,
        'numfavorited': len(favorited),
        'numclipped' : len(clipped),
        'numliked' : len(liked),
        'reviewed' : len(reviews),
        'count' : count,
        'distributions' : distributed_list,
        'rating' : int(rating)
    }
    return render(request, 'user-dashboard.html', context)

def index(request):
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None

    context = {'restaurant_rating_data': restaurant_rating_data, 'owner': owner}
    return render(request, "index.html", context)


def restaurant(request):
    id = request.GET.get('id')
    menu = FoodItem.objects.filter(menu__restaurant__name=id)
    featured = FoodItem.objects.filter(
        menu__restaurant__name=id).order_by('-likes')[:3]
    info = Restaurant.objects.filter(name=id)
    parse_mins(id)
    rating = getRating(id)
    num_reviews, reviews, count, distributed_list = getReviews(id,'restaurant')
    categories = getAndFormatCategories(id)
    uber_time, doordash_time = parse_mins(id)
    uber_link = Restaurant.objects.get(name = id).uberlink
    doordash_link = Restaurant.objects.get(name = id).doordashlink
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    context = {
        'menu': menu,
        'restaurant': info,
        'featured': featured,
        'categories': categories,
        'rating': rating,
        'reviews': reviews,
        'num': num_reviews,
        'count': count,
        'distributions': distributed_list,
        'name': id,
        'uber_time': uber_time,
        'doordash_time': doordash_time,
        'restaurant_rating_data': restaurant_rating_data,
        'uber_link' : uber_link,
        'doordash_link' : doordash_link,
        'owner': owner
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
def favorite(request, restaurant_id):
    restaurant = Restaurant.objects.get(name=restaurant_id)

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
            review.restaurant = Restaurant.objects.filter(
                name=request.POST.get('restaurant'))[:1].get()
            review.reviewer = User.objects.filter(
                username=request.POST.get('reviewer'))[:1].get()
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


@login_required
def register_owner(request):
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = request.user
            owner.save()
            return redirect('index')
    form = OwnerRegistrationForm()
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    return render(request=request, template_name="owner-register.html", context={"register_form": form, 'restaurant_rating_data': restaurant_rating_data})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    restaurants = Restaurant.objects.all()
    restaurant_rating_data = getRatings(restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user = request.user)
    except:
       owner = None
    return render(request=request, template_name="register.html", context={"register_form": form, 'restaurant_rating_data': restaurant_rating_data, "owner" : owner  })


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


@login_required
def create_restaurant(request):
    id = request.GET.get('id')
    restaurant = Restaurant.objects.filter(owner_id=id)
    owner = get_object_or_404(Owner, id=id)
    if request.user != owner.user:
        return redirect('index')
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        restaurant_name = request.POST.get('restaurant')
        if form_type == 'restaurant_form':
            form = RestaurantForm(request.POST, request.FILES)
            if form.is_valid():
                restaurant = form.save(commit=False)
                restaurant.owner = Owner.objects.filter(id=id)[:1].get()
                restaurant.save()
                return redirect('index')
        if form_type == 'fooditem_form':
            form = FoodItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.uber_price = float(request.POST.get('uber_price'))
                item.doordash_price = float(request.POST.get('doordash_price'))
                item.save()
                try:
                    menu = Menu.objects.get(restaurant__name=restaurant_name)
                except:
                    r = Restaurant.objects.get(name=restaurant_name)
                    menu = Menu(restaurant=r)
                    menu.save()
                menu.food_items.add(item)
                return redirect('index')
        if form_type == 'deals_form':
            form = DealsForm(request.POST, request.FILES,
                             restaurant_queryset=restaurant)
            if form.is_valid():
                deal = form.save(commit=False)
                deal.owner = Owner.objects.get(id=id)
                deal.save()
                return redirect('index')

    form = RestaurantForm()
    item_form = FoodItemForm()
    restaurant = Restaurant.objects.filter(owner_id=id)
    deals_form = DealsForm(restaurant_queryset=restaurant)

    owner_info = Owner.objects.filter(id=id)[0]
    restaurants = Restaurant.objects.filter(owner__id=id).all()
    restaurant_rating_data = getRatings(restaurants)
    restaurants_owned = len(restaurants)
    likes = getNumLikes(id)
    favorites = getNumFavorited(id)
    avg_rating = avgRatings(id)
    menu = getMenu(id)
    deals = Deals.objects.filter(owner_id=id)
    all_restaurants = Restaurant.objects.all()

    competition = getRatings(getCompetition(all_restaurants,restaurants))
    restaurant_rating_data2 = getRatings(all_restaurants)
    owner = ""
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None

    context = {
        'deals_form': deals_form,
        'deals': deals,
        'menu': menu,
        'form': form,
        'form2': item_form,
        'likes': likes,
        'favorites': favorites,
        'owner_info': owner_info,
        'restaurant_rating_data': restaurant_rating_data,
        'restaurant_rating_data2': restaurant_rating_data2,
        'restaurants_owned': restaurants_owned,
        'rating': avg_rating,
        'owner': owner,
        'competition' : competition
    }
    return render(request, 'owner-dashboard.html', context)
