from django.urls import path
from . import views
#app_name = 'shop'

urlpatterns = [
    path('register/', views.register, name="signup"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('profile/<int:user_id>', views.Profile, name="profile"),
    path('add/', views.addProduct, name="add"),
    path('view/<slug:product_slug>', views.viewProduct, name="view"),
    path('edit/<slug:product_slug>', views.editProduct, name="edit"),
    path('delete/<slug:product_slug>', views.deleteProduct, name="delete"),
    path('companies/', views.companylist, name="companylist"),
    path('cart/', views.cart, name="cart"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('orders/', views.orders, name="orders"),
    path('orders/<int:id>', views.viewOrder, name="order"),
    path('search/', views.search, name="search"),
]

'''path('profile/<int:user_id>/category/<int: category_id>/',
         views.filterByCategory, name="category"),
    path('profile/<int:user_id>/subcategory/<int: subcategory_id>/',
         views.filterBySubcategory, name="subcategory"),'''
