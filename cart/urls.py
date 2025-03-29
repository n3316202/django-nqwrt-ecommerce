from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = "cart"

urlpatterns = [
    path("cart/", include("cart.urls")),  # dev_13
]
