from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api import views

# dev_28
app_name = "api"

urlpatterns = [
    path("hello_world/", views.hello_world),
    path("hello_world_drf/", views.hello_world_drf),
    path("products/", views.products_api),
]
