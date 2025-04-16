from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers

from store.models import Category, Product


# 2. Serilaizer 객체의 주요 기능
# serialization
# deserialiaztion
# validation
# request / response 데이터 핸들링 ( to_internal_value() / to_representation() )
# nested serialization


# ✅ 주의할 점
# depth는 읽기 전용 출력만 가능해요.
# POST, PUT 요청에서 중첩된 객체를 직접 생성하거나 수정할 수는 없어요.
# 만약 쓰기도 원한다면 category_id 같은 별도 필드와 create() 오버라이드가 여전히 필요해요.


# 중첩구조 만들기
# dev_32
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


# def_29
# serializers.py 생성
# dev_32
# ✅ 2. ProductSerializer에서 Category를 중첩시키기
class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()  # 중첩으로 출력 #read_only=True
    # dev_32_2
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"  # fields = [ "id", "name", "price", "category", "is_sale","sale_price"]

    # dev_32_2
    # def create(self, validated_data):
    #     print("카테고리", validated_data)
    #     category_data = validated_data.pop("category")

    #     category, _ = Category.objects.get_or_create(
    #         **category_data
    #     )  # 카테고리 저장/조회
    #     product = Product.objects.create(**validated_data, category=category)
    #     return product

    # def update(self, instance, validated_data):
    #     category_data = validated_data.pop("category", None)
    #     if category_data:
    #         category, _ = Category.objects.get_or_create(**category_data)
    #         instance.category = category

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance
