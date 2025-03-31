from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from orders import views

# dev_24
app_name = "orders"

urlpatterns = [
    path("create/", views.orders_create, name="orders_create"),
]
