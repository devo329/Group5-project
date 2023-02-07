from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("loading/", views.loading_screen,),
    path("restaurant/", views.restaurant,name="restaurants"),
]