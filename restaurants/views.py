from django.shortcuts import render

import restaurants
#from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from django.shortcuts import render

def index(request):
    restaurants = Restaurant.objects.values()
    context = {'all_restaurant' : restaurants}
    return render(request, "index.html", context)

def restaurant(request):
    id = request.GET.get('id')
    menu = FoodItem.objects.filter(menu__restaurant__name = id)
    info = Restaurant.objects.filter(name = id)
    context = {'menu' : menu,'restaurant': info}
    return render(request, "restaurant.html", context)