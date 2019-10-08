from django import forms
from .models import *


class CreateNewProduct(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=1000)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    rate = forms.FloatField()
    in_stock = forms.IntegerField()
    product_image = forms.ImageField()
