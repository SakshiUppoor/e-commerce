from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, auth
from .models import *
from django.urls import reverse
from accounts.models import *
from .forms import CreateNewProduct
# Create your views here.


def home(request):
    companies = Company.objects.all()
    products = Product.objects.all().order_by('-id')
    context = {
        'companies': companies,
        'products': products,
    }
    return render(request, "home.html", context)


def addProduct(request):
    if request.user.is_authenticated:
        if request.user.is_company:
            form = CreateNewProduct()
            '''if request.method == 'POST':
                new_product = Product()
                new_product.name = request.POST['product_name']
                new_product.description = request.POST['description']
                new_product.rate = request.POST['rate']
                new_product.in_stock = request.POST['in_stock']
                new_product.company = Company.objects.filter(
                    user=request.user).first()
                new_product.product_image = request.POST['pic']
                new_product.save()
                return HttpResponseRedirect(reverse('shop:home'))
            context = {
                'categories' : Category.objects.all(),
                'subcategories' : Subcategory.objects.all(),
            }
            return render(request, "addProduct.html",context)'''
            if request.method == 'POST':
                form = CreateNewProduct(request.POST, request.FILES)
                if form.is_valid():
                    print("hrllo")
                    new_product = Product()
                    new_product.name = form.cleaned_data['name']
                    new_product.product_image = form.cleaned_data['product_image']
                    new_product.description = form.cleaned_data['description']
                    new_product.rate = form.cleaned_data['rate']
                    new_product.in_stock = form.cleaned_data['in_stock']
                    new_product.company = Company.objects.filter(
                        user=request.user).first()
                    new_product.subcategory = form.cleaned_data['subcategory']
                    new_product.save()
                    return HttpResponse('image upload success')
            context = {
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.all(),
                'form': form,
            }
            return render(request, "addProduct.html", context)
        return render(request, "404.html")
    return HttpResponseRedirect(reverse('accounts:user_login'))


def editProduct(request, product_slug):
    if request.user.is_authenticated:
        if request.user.is_company:
            if request.method == "POST":
                product = Product.objects.filter(slug=product_slug)[0]
                product.name = request.POST['product_name']
                product.description = request.POST['description']
                product.rate = request.POST['rate']
                product.in_stock = request.POST['in_stock']
                product.save()
                return HttpResponseRedirect(reverse('shop:home'))
            else:
                product = Product.objects.filter(slug=product_slug)[0]
                context = {
                    'p': product,
                }
                return render(request, "editProduct.html", context)
        return render(request, "404.html")
    return HttpResponseRedirect(reverse('accounts:user_login'))


def deleteProduct(request, product_slug):
    if request.user.is_company:
        if request.method == "POST":
            Product.objects.filter(slug=product_slug).delete()
            return HttpResponseRedirect(reverse('shop:home'))
        else:
            product = Product.objects.filter(slug=product_slug)[0]
            context = {
                'product': product,
            }
            return render(request, "deleteProduct.html", context)
    return render(request, "404.html")


def viewProduct(request, product_slug):
    product = Product.objects.filter(slug=product_slug)[0]
    context = {
        'product': product,
    }
    return render(request, "viewProduct.html", context)
