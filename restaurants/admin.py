from django.contrib import admin

from restaurants.models import Restaurant, Owner, Menu, FoodItem, Reviews,Deals

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Owner)
admin.site.register(Menu)
admin.site.register(FoodItem)
admin.site.register(Reviews)
admin.site.register(Deals)