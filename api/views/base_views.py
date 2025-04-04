from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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



