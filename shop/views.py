from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from .models import *
from django.urls import reverse
from .forms import CreateNewProduct
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


def register(request):

    if request.method == 'POST':
        if 'customerCreate' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                '''if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return HttpResponseRedirect(reverse('register'))
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return HttpResponseRedirect(reverse('signup'))
                else:'''
                user = User.objects.create_user(
                    username=email, email=email, password=password1, first_name=first_name, last_name=last_name, is_customer=True)
                user.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.info(request, 'Password not matching')
                return HttpResponseRedirect(reverse('signup'))
            return HttpResponseRedirect(reverse('login'))
        elif 'companyCreate' in request.POST:
            first_name = request.POST['company_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(first_name=first_name).exists():
                    messages.info(request, 'Name Taken')
                    return HttpResponseRedirect(reverse('signup'))
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return HttpResponseRedirect(reverse('signup'))
                else:
                    user = User.objects.create_user(
                        username=email, email=email, password=password1, first_name=first_name, is_company=True)
                    user.save()
                    return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.info(request, 'Password not matching')
                return HttpResponseRedirect(reverse('signup'))
            return HttpResponseRedirect(reverse('user_login'))

    else:
        return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or password incorrect')
            return redirect('user_login')
    else:
        return render(request, 'login.html')


def user_logout(request):
    auth.logout(request)
    return redirect(reverse('user_login'))


''' under-construction'''


def Profile(request, user_id):
    this_user = User.objects.get(id=user_id)
    if this_user.is_company:
        items = Product.objects.filter(company=this_user.company)
        context = {
            'items': items,
            'company': Company.objects.filter(user=this_user).first(),
        }
        return render(request, "companypage.html", context)
    elif this_user.is_customer:
        context = {

        }
        return render(request, "customerProfile.html", context)
    return render(request, "404.html")


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
                return HttpResponseRedirect(reverse('home'))
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
                    return HttpResponseRedirect(reverse('home'))
            context = {
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.all(),
                'form': form,
            }
            return render(request, "addProduct.html", context)
        return render(request, "404.html")
    return HttpResponseRedirect(reverse('user_login'))


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
                return HttpResponseRedirect(reverse('home'))
            else:
                product = Product.objects.filter(slug=product_slug)[0]
                context = {
                    'p': product,
                }
                return render(request, "editProduct.html", context)
        return render(request, "404.html")
    return HttpResponseRedirect(reverse('user_login'))


def deleteProduct(request, product_slug):
    if request.user.is_company:
        if request.method == "POST":
            Product.objects.filter(slug=product_slug).delete()
            return HttpResponseRedirect(reverse('home'))
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
