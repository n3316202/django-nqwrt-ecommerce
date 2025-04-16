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
    category = CategorySerializer()  # 중첩으로 출력 #read_only=True

    # category_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), write_only=True
    # )

    class Meta:
        model = Product
        fields = "__all__"  # fields = [ "id", "name", "price", "category", "is_sale","sale_price"]
        # fields = [
        #     "id",
        #     "name",
        #     "price",
        #     "description",
        #     "image",
        #     "is_sale",
        #     "sale_price",
        #     "category",  # 출력용 (중첩)
        #     # "category_id",  # 입력용 (ID)
        # ]

    def create(self, validated_data):
        # category_id로 받은 객체 꺼내서 처리
        # ✅ pop() 함수 기본 설명
        # my_dict = {"name": "Tom", "age": 25}
        # age = my_dict.pop("age")
        # print(age)         # 출력: 25
        # print(my_dict)     # 출력: {'name': 'Tom'}
        # category = validated_data.pop("category_id")
        # product = Product.objects.create(**validated_data, category=category)
        # return product
        print("카테고리", validated_data)
        category_data = validated_data.pop("category")

        # category	조회되었거나 새로 생성된 Category 인스턴스
        # created	True면 새로 생성된 것이고, False면 기존에 있던 것
        category, _ = Category.objects.get_or_create(
            **category_data
        )  # 카테고리 저장/조회
        product = Product.objects.create(**validated_data, category=category)
        return product

    # def update(self, instance, validated_data):
    #     category_data = validated_data.pop("category", None)
    #     if category_data:
    #         category, _ = Category.objects.get_or_create(**category_data)
    #         instance.category = category

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance

    # dev_31
    # 가격은 0 이상 1000 이하
    def validate_price(self, value):
        if value < 1000:
            raise serializers.ValidationError("가격은 0 이상이어야 합니다.")
        if value > 20000:
            raise serializers.ValidationError("가격은 20000 이하여야 합니다.")
        return value

    # 이름은 3자 이상 100자 이하
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("상품 이름은 최소 3자 이상이어야 합니다.")
        if len(value) > 100:
            raise serializers.ValidationError("상품 이름은 100자를 초과할 수 없습니다.")
        return value

    def validate(self, data):
        is_sale = data.get("is_sale")
        sale_price = data.get("sale_price")

        if is_sale:
            # 세일 중이면 sale_price는 반드시 필요하고 0보다 커야 함
            if sale_price is None or sale_price <= 0:
                raise serializers.ValidationError(
                    {"sale_price": "세일 중일 경우 sale_price는 0보다 커야 합니다."}
                )
        else:
            # 세일이 아니면 sale_price는 아예 없어야 함 (자동 무시하거나 경고)
            if sale_price and sale_price > 0:
                raise serializers.ValidationError(
                    {
                        "sale_price": "is_sale이 false 이면 sale_price를 지정할 수 없습니다."
                    }
                )

        return data


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
