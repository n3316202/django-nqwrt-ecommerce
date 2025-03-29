from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "store"
# dev_1
urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),  # dev_8
    path("product/<int:product_id>", views.product, name="product"),  # dev_13
    # 변수 foo 의 의미  참고:https://namu.wiki/w/foo #dev_14
    path("category/<str:foo>", views.category, name="category"),
    path("category_summary/", views.category_summary, name="category_summary"),
]
