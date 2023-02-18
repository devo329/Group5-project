from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register_request, name="register"),
    path("", views.index, name="index"),
    path("owner/dashboard", views.create_restaurant, name = 'create-restaurant'),
    path("loading/restaurant/", views.loading_screen,),
    path("restaurant/", views.restaurant,name='restaurant'),
    path('review/submit/', views.addReview, name='review_submit'),
    path('favorite/<restaurant_id>', views.favorite, name='favorite'),
    path('like/<int:item_id>/<restaurant_id>', views.like, name='like'),
    path("logout", views.logout_request, name= "logout"),
]