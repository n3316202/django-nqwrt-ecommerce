from django.contrib import admin
from django.urls import path, include
from cart import views

# dev_15
app_name = "cart"

urlpatterns = [
    path("", views.cart_summary, name="cart_summary"),  # dev_18
    path("add/", views.cart_add, name="cart_add"),
    path("delete/", views.cart_delete, name="cart_delete"),  # dev_19
    path("update/", views.cart_update, name="cart_update"),  # dev_19
]
