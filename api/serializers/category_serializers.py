from rest_framework import serializers
from store.models import Category


# dev_32_3
class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    from api.serializers.product_serializers import ProductSimpleSerializer

    products = ProductSimpleSerializer(
        many=True, read_only=True
    )  # related_name=products

    class Meta:
        model = Category
        fields = "__all__"
