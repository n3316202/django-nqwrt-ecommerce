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


# def_29
# serializers.py 생성
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"  # fields = [ "id", "name", "price", "category", "is_sale","sale_price"]
        depth = 1  # dev_32 ForeignKey 필드 자동 직렬화

    # def validate_price(self, value):
    #     if value > 1000:
    #         raise serializers.ValidationError("Price must be a positive value.")
    #     return value

    # def validate_name(self, value):
    #     if len(value) > 3:
    #         raise serializers.ValidationError("Name must be at most 3 characters long.")
    #     return value


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=100)
#     price = serializers.IntegerField()
#     # category = serializers.IntegerField()
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     description = serializers.CharField(
#         max_length=250, required=False, allow_blank=True, allow_null=True
#     )
#     image = serializers.ImageField()
#     is_sale = serializers.BooleanField()
#     sale_price = serializers.IntegerField()


# dev_31
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"


# dev_32
# CategorySerializer에서 일대다 관계 보이게 하기
# 역방향 참조
class CategorySerializer(serializers.ModelSerializer):
    # dev_33
    # products = ProductSerializer(many=True, read_only=True) #related_name=products

    class Meta:
        model = Category
        fields = "__all__"
