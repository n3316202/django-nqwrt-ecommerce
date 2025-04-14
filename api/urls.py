from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views import *

# dev_28
app_name = "api"

urlpatterns = [
    path("hello-world/", hello_world),
    path("hello-world-drf/", hello_world_drf),
    # dev_29
    path("products-all/", products_all_drf),
]
