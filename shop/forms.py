from django import forms
from .models import *


class CreateNewProduct(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=1000)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    rate = forms.FloatField()
    in_stock = forms.IntegerField()
    product_image = forms.ImageField(required=False)


class CompanyProfile(forms.Form):
    profile_image = forms.ImageField(required=False)
    name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'myfieldclass'}))
    description = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'myfieldclass'}))
    header_image = forms.ImageField(required=False)


class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'rate', 'in_stock', 'product_image']
