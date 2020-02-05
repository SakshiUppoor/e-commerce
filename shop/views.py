from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from .models import *
from django.urls import reverse
from .forms import CreateNewProduct, CompanyProfile, EditProduct
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import ListView
import requests

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
            if not User.objects.filter(email=email).exists():
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
                    return HttpResponseRedirect(reverse('user_login'))
                else:
                    messages.info(request, 'Password not matching')
                    return HttpResponseRedirect(reverse('signup'))
            else:
                messages.info(request, 'Email taken')
                return HttpResponseRedirect(reverse('signup'))
            return HttpResponseRedirect(reverse('user_login'))
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
            return redirect(reverse('companylist'))
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
        company = Company.objects.filter(user=this_user).first()
        form = CompanyProfile(initial={
            'name': company.user.first_name,
            'description': company.description,
        })
        editform = EditProduct()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        if request.method == 'POST':
            form = CompanyProfile(request.POST, request.FILES)
            if form.is_valid():
                company.user.first_name = form.cleaned_data['name']
                if 'profile_image' in request.FILES:
                    company.user.profile_images = request.FILES['profile_image']

                if 'header_image' in request.FILES:
                    company.header = request.FILES['header_image']
                company.description = form.cleaned_data['description']
                company.user.save()
                company.save()
        items = Product.objects.filter(company=this_user.company)
        context = {
            'items': items,
            'company': company,
            'form': form,
            'categories': categories,
            'subcategories': subcategories,
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
                    if form.data['product_image']:
                        new_product.product_image = form.cleaned_data['product_image']
                    new_product.description = form.cleaned_data['description']
                    new_product.rate = form.cleaned_data['rate']
                    new_product.in_stock = form.cleaned_data['in_stock']
                    new_product.company = Company.objects.filter(
                        user=request.user).first()
                    new_product.subcategory = form.cleaned_data['subcategory']
                    new_product.save()
                    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
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
                return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
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
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
        else:
            product = Product.objects.filter(slug=product_slug)[0]
            context = {
                'product': product,
            }
            return render(request, "deleteProduct.html", context)
    return render(request, "404.html")


def viewProduct(request, product_slug):
    product = Product.objects.filter(slug=product_slug)[0]
    if request.method == "POST":
        if request.user.is_authenticated:
            if 'addToCart' in request.POST:
                cartitem = CartItem.objects.filter(
                    product=product, cart=request.user.cart)
                print(cartitem.exists)
                if cartitem.exists():
                    cartitem = cartitem[0]
                    cartitem.quantity = cartitem.quantity + \
                        int(request.POST['qty'])
                    cartitem.cost = cartitem.quantity * product.rate
                    cartitem.save()
                else:
                    newcartitem = CartItem()
                    newcartitem.quantity = int(request.POST['qty'])
                    newcartitem.product = product
                    newcartitem.cart = request.user.cart
                    newcartitem.cost = int(
                        request.POST['qty']) * product.rate
                    newcartitem.save()
                return HttpResponseRedirect(reverse('cart'))
            elif 'addToWishlist' in request.POST:
                wishlistItem = WishlistItem.objects.filter(
                    user=request.user, product=product)
                print(wishlistItem.exists())
                if not wishlistItem.exists():
                    newitem = WishlistItem()
                    newitem.user = request.user
                    newitem.product = product
                    newitem.save()
                    print('added!')
                else:
                    wishlistItem = wishlistItem[0].delete()
                    print('deleted!')
            return(HttpResponseRedirect(reverse('view', kwargs={'product_slug': product_slug})))

        else:
            return render(request, 'login.html')

    context = {
        'product': product,
        'wishitem': WishlistItem.objects.filter(
            user=request.user, product=product).exists,
    }
    return render(request, "productinfo.html", context)


class ProductView(ListView):
    template_name = "home.html"
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context


def companylist(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'companylistpage.html', context)


def cart(request):
    if request.method == "POST":
        if 'submit' in request.POST:
            cartItems = CartItem.objects.filter(
                is_saved_for_later=False, cart=request.user.cart)
            address = request.POST['address']
            order = Order()
            order.address = address
            order.save()
            for item in cartItems:
                orderitem = OrderItem()
                orderitem.product = item.product
                if (item.product.in_stock >= item.quantity):
                    item.product.in_stock -= item.quantity
                    orderitem.quantity = item.quantity
                else:
                    orderitem.quantity = item.product.in_stock
                    item.product.in_stock = 0
                item.product.save()
                orderitem.order = order
                orderitem.order_item_cost = item.cost
                order.total += item.cost
                order.save()
                orderitem.save()
                item.delete()
            return(HttpResponseRedirect(reverse('order', kwargs={'id': order.id})))

        else:
            id = int(request.POST['itemId'])
            cartitem = CartItem.objects.filter(id=id)[0]
            if 'subtract' in request.POST:
                if cartitem.quantity != 1:
                    cartitem.quantity -= 1
            elif 'add' in request.POST:
                cartitem.quantity += 1
            elif 'save' in request.POST:
                cartitem.is_saved_for_later = True
            elif 'cart' in request.POST:
                cartitem.is_saved_for_later = False

            cartitem.save()
            return(HttpResponseRedirect(reverse('cart')))

    if request.user.is_authenticated and request.user.is_customer:
        cartItems = CartItem.objects.filter(
            is_saved_for_later=False, cart=request.user.cart)
        total_cost = 0
        for item in cartItems:
            total_cost += item.cost
        context = {
            'cartItems': cartItems,
            'savedItems': CartItem.objects.filter(is_saved_for_later=True, cart=request.user.cart),
            'total_cost': total_cost
        }
        return render(request, 'cart.html', context)
    else:
        if request.user.is_company:
            return(HttpResponseRedirect(reverse('user_logout')))
        return(HttpResponseRedirect(reverse('user_login')))


def wishlist(request):
    if request.user.is_authenticated and request.user.is_customer:
        print(WishlistItem.objects.filter(user=request.user))
        context = {
            'wishListItems': WishlistItem.objects.filter(user=request.user)
        }
        return render(request, 'wishlist.html', context)
    else:
        if request.user.is_company:
            return(HttpResponseRedirect(reverse('user_logout')))
        return(HttpResponseRedirect(reverse('user_login')))


def orders(request):
    return render(request, 'orders.html')


def viewOrder(request, id):
    if request.user.is_authenticated and request.user.is_customer:
        order = Order.objects.get(id=id)
        context = {
            'orderItems': OrderItem.objects.filter(order=order)
        }
        return render(request, 'vieworder.html', context)
    else:
        if request.user.is_company:
            return(HttpResponseRedirect(reverse('user_logout')))
        return(HttpResponseRedirect(reverse('user_login')))


def filterByCategory(request, user_id, category_id):
    this_user = User.objects.get(id=user_id)
    if this_user.is_company:
        company = Company.objects.filter(user=this_user).first()
        form = CompanyProfile(initial={
            'name': company.user.first_name,
            'description': company.description,
        })
        editform = EditProduct()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        if request.method == 'POST':
            form = CompanyProfile(request.POST, request.FILES)
            if form.is_valid():
                company.user.first_name = form.cleaned_data['name']
                if 'profile_image' in request.FILES:
                    company.user.profile_images = request.FILES['profile_image']

                if 'header_image' in request.FILES:
                    company.header = request.FILES['header_image']
                company.description = form.cleaned_data['description']
                company.user.save()
                company.save()
        category = Category.objects.get(id=category_id)
        items = Product.objects.filter(
            company=this_user.company, subcategory=category.subcategory)
        context = {
            'items': items,
            'company': company,
            'form': form,
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request, "companypage.html", context)
    elif this_user.is_customer:
        context = {

        }
        return render(request, "customerProfile.html", context)
    return render(request, "404.html")


def filterBySubcategory(request, user_id, subcategory_id):
    this_user = User.objects.get(id=user_id)
    if this_user.is_company:
        company = Company.objects.filter(user=this_user).first()
        form = CompanyProfile(initial={
            'name': company.user.first_name,
            'description': company.description,
        })
        editform = EditProduct()
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        if request.method == 'POST':
            form = CompanyProfile(request.POST, request.FILES)
            if form.is_valid():
                company.user.first_name = form.cleaned_data['name']
                if 'profile_image' in request.FILES:
                    company.user.profile_images = request.FILES['profile_image']

                if 'header_image' in request.FILES:
                    company.header = request.FILES['header_image']
                company.description = form.cleaned_data['description']
                company.user.save()
                company.save()
        subcategory = Subcategory.objects.get(id=subcategory_id)
        items = Product.objects.filter(
            company=this_user.company, subcategory=subcategory)
        context = {
            'items': items,
            'company': company,
            'form': form,
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request, "companypage.html", context)
    elif this_user.is_customer:
        context = {

        }
        return render(request, "customerProfile.html", context)
    return render(request, "404.html")


def search(request):
    if request.method=="POST":
        print(request.POST)
        if 'search' in request.POST:
            print("hi")
            query = request.POST['query']
            query_list = []
            if 'searched_for' in request.COOKIES:
                query_list = request.COOKIES['searched_for'] + "," + query
            else:
                query_list = query
            response = HttpResponseRedirect(reverse('search'))
            response.set_cookie('searched_for', query_list)
            return response
    print(request.COOKIES)
    query_list = []
    if 'searched_for' in request.COOKIES:
        query_list = request.COOKIES['searched_for']
    print(query_list)
    if len(query_list) is not 0:
        query_list = query_list.split(',')
    context = {
        'query_list': query_list,
    }
    return render(request, 'search.html', context)
 