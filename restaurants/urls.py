from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("loading/restaurant/", views.loading_screen,),
    path("restaurant/", views.restaurant,name='restaurant'),
    path('review/submit/', views.addReview, name='review_submit'),
    path('like/<int:item_id>/<restaurant_id>', views.like, name='like'),
]