from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from payment import views


# dev_25
app_name = "payment"

urlpatterns = [
    path("process/", views.payment_process, name="payment_process"),
]
