from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# dev_30
from .views import base_views, product_views

# dev_28
app_name = "api"

# dev_30
urlpatterns = [
    # base_views.py
    path("hello-world/", base_views.hello_world),
    path("hello-world-drf/", base_views.hello_world_drf),
    path("core-product-drf/", base_views.core_serializer_drf),
    # product_views.py
    path("products/", product_views.products_api),
    path("product/<int:pk>/", product_views.product_api),  # dev_30
]
