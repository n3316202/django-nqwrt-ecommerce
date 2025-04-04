from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product
from api.serializers import ProductSerializer

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
# @api_view(["GET"])
# def products_api(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)

#     return Response(serializer.data)


# dev_29 추가 되도록
@api_view(["GET", "POST"])
def products_api(request):

    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # 디시리얼라이져
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
