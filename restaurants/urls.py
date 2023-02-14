from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name="index"),
    path("loading/restaurant/", views.loading_screen,),
    path("restaurant/", views.restaurant,name='restaurant'),
    path('like/<int:item_id>/<restaurant_id>', views.like, name='like'),
]