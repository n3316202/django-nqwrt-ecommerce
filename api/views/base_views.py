from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from store.models import Product
from api.serializers import ProductSerializer

from django.test import TestCase
from store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers
from django.http import JsonResponse

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


# DRF Serializer를 쓰는 게 훨씬 유연하고 강력
# Django 내장 기능이고, 단순히 QuerySet을 JSON, XML 등 문자열로 직렬화하고 싶을 때 사용합니다.
def core_serializer_drf(request):
    products = Product.objects.all()
    data = serializers.serialize("json", products)  # JSON 문자열로 직렬화
    return JsonResponse(data, safe=False)  # safe=False로 리스트 반환 허용
