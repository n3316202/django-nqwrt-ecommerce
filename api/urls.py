from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# dev_30
from .views import base_views, product_views, category_views

# dev_28
app_name = "api"

# dev_30
urlpatterns = [
    # base_views.py
    path("hello_world/", base_views.hello_world),
    path("hello_world_drf/", base_views.hello_world_drf),
    # product_views.py
    path("products/", product_views.products_api),
    path("product/<int:pk>/", product_views.product_api),  # dev_30
    # product_views.py #dev_31
    path("categories/", category_views.CategoriesAPI.as_view()),  # dev_31
    path("category/<int:pk>/", category_views.CategoryAPI.as_view()),  # dev_31
]
