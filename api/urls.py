from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views import hello_world, hello_world_drf

# dev_28
app_name = "api"

urlpatterns = [
    path("hello_world/", hello_world),
    path("hello_world_drf/", hello_world_drf),
]
