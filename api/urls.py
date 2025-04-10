from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views.cart_views import CartAPIView

# dev_30
from .views import base_views, product_views, category_views

# dev_34
from rest_framework import routers

# dev_28
app_name = "api"

# dev_35
router = routers.DefaultRouter()
router.register(r"categories", category_views.CategoryViewSet)

# dev_30
urlpatterns = [
    # base_views.py
    path("hello_world/", base_views.hello_world),
    path("hello_world_drf/", base_views.hello_world_drf),
    # product_views.py
    path("products/", product_views.products_api),
    path("product/<int:pk>/", product_views.product_api),  # dev_30
    # dev_31
    # path("categories/", category_views.CategoriesAPI.as_view()),  # dev_31
    # path("category/<int:pk>/", category_views.CategoryAPI.as_view()),  # dev_31
    # dev_33
    # path("categories/", category_views.CategoriesMixins.as_view()),  # dev_33
    # path("category/<int:pk>/", category_views.CategoryMixins.as_view()),  # dev_33
    # path("categories/", category_views.CategoriesAPI.as_view()),  # dev_34
    # path("category/<int:pk>/", category_views.CategoryAPI.as_view()),  # dev_34
    # dev_34 http://127.0.0.1:8000/api/categories/
    # 이렇게 하면 다음 경로들이 자동으로 만들어집니다:
    # GET /categories/
    # POST /categories/
    # GET /categories/<pk>/
    # PUT /categories/<pk>/
    # PATCH /categories/<pk>/
    # DELETE /categories/<pk>/
    path("", include(router.urls)),
    path("cart/", CartAPIView.as_view(), name="api_cart"),
    # dev_38
    path("auth/", include("djoser.urls")),  # 회원가입, 비밀번호 변경 등
    path("auth/", include("djoser.urls.jwt")),  # JWT 로그인/로그아웃, 토큰 갱신 등
]
