from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from store.models import Product, Category
from api.serializers.product_serializers import ProductSerializer

# Create your views here.


# dev_29 추가 되도록
@api_view(["GET", "POST"])
def products_api(request):

    if request.method == "GET":
        products = Product.objects.all()
        # many=True ➜ 여러 개의 인스턴스 (QuerySet, 리스트 등)
        # many=False (기본값) ➜ 단일 인스턴스
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # dev_32_2

    # 디시리얼라이져
    # if request.method == "POST":
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # dev_32_2
    #     {
    #     "category": {
    #         "name": "과일"
    #     },
    #     "name": "오렌지",
    #     "price": "12000.00",
    #     "description": "파이썬 책입니다.",
    #     "image": null,
    #     "is_sale": false,
    #     "sale_price": 0
    # }
    if request.method == "POST":
        # request.data 는 기본적으로 불변임
        data = request.data.copy()

        # category 정보 추출 후 제거
        category_data = data.pop("category")

        # print("리퀘스트 데이타", request.data["category"])
        category_data = request.data["category"]

        # get_or_create 는 dict 형식으로 받기 때문에 category_data는 리스트일 수 있어서 주의
        if isinstance(category_data, list):
            category_data = category_data[0]

        category, _ = Category.objects.get_or_create(
            **category_data
        )  # 카테고리 저장/조회

        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)  # 수동으로 카테고리 지정

        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def product_api(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
