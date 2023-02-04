from multiprocessing import context
from django.shortcuts import render
#from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from django.shortcuts import render

def index(request):
    restaurants = Restaurant.objects.all()
    context = {'all_restaurant' : restaurants}
    return render(request, "index.html", context)