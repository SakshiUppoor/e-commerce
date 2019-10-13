from django.urls import path
from . import views
#app_name = 'shop'

urlpatterns = [
    path('register/', views.register, name="signup"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('profile/<int:user_id>', views.Profile, name="profile"),
    path('', views.home, name="home"),
    path('add/', views.addProduct, name="add"),
    path('view/<slug:product_slug>', views.viewProduct, name="view"),
    path('edit/<slug:product_slug>', views.editProduct, name="edit"),
    path('delete/<slug:product_slug>', views.deleteProduct, name="delete"),
]
