from rest_framework import serializers
from store.models import Category, Product


# dev_32_3
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    from api.serializers.category_serializers import CategorySimpleSerializer

    category = CategorySimpleSerializer()

    class Meta:
        model = Product
        fields = "__all__"
        # fields = ["id", "name", "category"]
        # dev_32 ForeignKey 필드 자동 직렬화
        # ForeignKey에 해당 되는 모델을 시리얼라이즈로 만들필요 없이 자동으로 직렬화(json) 해줌
        # 단점: depth 가 깊어 지면 속도에 문제가 생김
        # 기본적으로 read_only 임
        # depth = 1

    def create(self, validated_data):
        category_data = validated_data.pop("category")

        # 카테고리 저장/조회
        category, _ = Category.objects.get_or_create(**category_data)
        product = Product.objects.create(**validated_data, category=category)

        return product
