from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# dev_8
app_name = "accounts"

urlpatterns = [
    # django.contrib.auth앱의 LoginView 클래스를 활용했으므로 별도의 views.py 파일 수정이 필요 없음
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register_user, name="register_user"),
]
