from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static

from payment import views


# dev_26
app_name = "payment"

urlpatterns = [
    path("process/", views.payment_process, name="payment_process"),
]
