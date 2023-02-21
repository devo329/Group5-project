
from django import forms

from Price_Comp.settings import BASE_DIR
from .models import FoodItem, Restaurant, Reviews,Owner,Deals
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import os


class DealsForm(forms.ModelForm):
    class Meta:
        model = Deals
        fields = ['name', 'code', 'restaurant', 'image_name']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'code': forms.TextInput(attrs={'class': 'form-control'}),
        'restaurant': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        restaurant_queryset = kwargs.pop('restaurant_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['restaurant'].queryset = restaurant_queryset

    image_name = forms.FileField(required=True)

    def save(self, commit=True):
        MEDIA_ROOT = os.path.join(BASE_DIR, 'restaurants/static/deals')
        isExist = os.path.exists(MEDIA_ROOT)
        if not isExist:
            os.makedirs(MEDIA_ROOT)

        deal = super(DealsForm, self).save(commit=False)

        image_file = self.cleaned_data.get('image_name', None)
        if image_file:
            file_path = os.path.join(MEDIA_ROOT, image_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            deal.image_name = image_file.name

        if commit:
            deal.save()
        return deal

class OwnerRegistrationForm(forms.ModelForm):
     class Meta:
        model = Owner
        fields = ['first_name', 'last_name']
        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating', 'review']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'image_name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
        }

    image_name = forms.FileField(required=True)
    def save(self, commit=True):
        MEDIA_ROOT = os.path.join(BASE_DIR, 'restaurants/static/fooditem')
        fooditem = super(FoodItemForm, self).save(commit=False)

        image_file = self.cleaned_data.get('image_name', None)
        if image_file:
            file_path = os.path.join(MEDIA_ROOT, image_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            fooditem.image_name = image_file.name

        if commit:
            fooditem.save()
        return fooditem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'cuisine', 'price_range', 'uber_delivery_time', 'doordash_delivery_time', 'image_name', 'banner_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'cuisine': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.TextInput(attrs={'class': 'form-control'}),
            'uber_delivery_time': forms.TextInput(attrs={'class': 'form-control'}),
            'doordash_delivery_time': forms.TextInput(attrs={'class': 'form-control'}),
        }


    image_name = forms.FileField(required=True)
    banner_name = forms.FileField(required=True)

    def save(self, commit=True):
        RESTAURANT_ROOT = os.path.join(BASE_DIR, 'restaurants/static/restaurant')
        BANNER_ROOT = os.path.join(BASE_DIR, 'restaurants/static/banners')
        restaurant = super(RestaurantForm, self).save(commit=False)

        image_file = self.cleaned_data.get('image_name', None)
        if image_file:
            file_path = os.path.join(RESTAURANT_ROOT, image_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            restaurant.image_name = image_file.name

        image_file = self.cleaned_data.get('banner_name', None)
        if image_file:
            file_path = os.path.join(BANNER_ROOT, image_file.name)
            print(image_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            restaurant.banner_name = image_file.name

        if commit:
            restaurant.save()
        return restaurant


