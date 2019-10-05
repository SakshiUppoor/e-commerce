from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.home, name="home"),
    path('add/', views.addProduct, name="add"),
    path('view/<slug:product_slug>', views.viewProduct, name="view"),
    path('edit/<slug:product_slug>', views.editProduct, name="edit"),
    path('delete/<slug:product_slug>', views.deleteProduct, name="delete"),
]
