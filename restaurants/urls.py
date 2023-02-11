from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/", views.restaurant,name='restaurant'),
    path('like/<int:item_id>/<restaurant_id>', views.like, name='like'),
]