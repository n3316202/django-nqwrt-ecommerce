from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product
from django.core import serializers

# Create your views here.


# dev_28
# 기존방식
def hello_world(request):
    return HttpResponse("Hello World!")


# https://www.django-rest-framework.org/api-guide/views/#api_view
# DRF 방식
@api_view(["GET"])
def hello_world_drf(request):
    return Response({"message": "Hello World!"})


# dev_29
@api_view(["GET"])
def products_all_drf(request):
    products = Product.objects.all()
    data = serializers.serialize("json", products)
    return HttpResponse(data, content_type="application/json")
