from django.test import TestCase
from store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers


# dev_29
# Create your tests here.
class SerializerTest(TestCase):

    def setUp(self):
        # 카테고리 생성
        self.category = Category.objects.create(name="Electronics")

        # 테스트 이미지 생성
        self.image = SimpleUploadedFile(
            name="1.png", content=b"some image content", content_type="image/jpeg"
        )

        # Product 생성
        self.product = Product.objects.create(
            name="Test Product",
            price=999.99,
            description="This is a test product.",
            image=self.image,
            category=self.category,
            is_sale=True,
            sale_price=899,
        )

    # dev_29 serializers 사용법
    def test_product_serialization(self):
        products = Product.objects.all()
        data = serializers.serialize("json", products)
        print(data)
