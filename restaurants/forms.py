from django import forms
from .models import FoodItem, Reviews

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['rating', 'review']
