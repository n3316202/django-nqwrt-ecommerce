from django.test import TestCase

# Create your tests here.


def add(num1, num2):
    return num1 + num2


def minus(num1, num2):
    return num1 - num2


dic_calculator = {
    "add/": add,
    "minus/": minus,
}


class AnyTest(TestCase):
    def setUp(self):
        pass

    def test_calculator(self):
        url = "add/"
        print(url)
        print(dic_calculator[url](3, 2))


from django.test import TestCase
from store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import serializers

# class SerializerTest(TestCase):

#     def setUp(self):
#         # 카테고리 생성
#         self.category = Category.objects.create(name="Electronics")

#         # 테스트 이미지 생성
#         self.image = SimpleUploadedFile(
#             name="1.png", content=b"some image content", content_type="image/jpeg"
#         )

#         # Product 생성
#         self.product = Product.objects.create(
#             name="Test Product",
#             price=999.99,
#             description="This is a test product.",
#             image=self.image,
#             category=self.category,
#             is_sale=True,
#             sale_price=899,
#         )

#     # dev_29 serializers 사용법
#     def test_product_serialization(self):
#         products = Product.objects.all()
#         data = serializers.serialize("json", products)
#         print(data)

from django.test import TestCase
from api.serializers import ProductSerializer
from store.models import Category, Product


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_valid_product_data(self):
        data = {
            "name": "TV",
            "price": 999.99,
            "description": "A large smart TV.",
            "category": self.category.id,
            "is_sale": True,
            "sale_price": 500,
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "TV")

    def test_price_too_high(self):
        data = {
            "name": "TV",
            "price": 1500,
            "description": "Too expensive",
            "category": self.category.id,
            "is_sale": False,
            "sale_price": 0,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_name_too_short(self):
        data = {
            "name": "TV",  # Too short (<3)
            "price": 500,
            "description": "Short name",
            "category": self.category.id,
            "is_sale": False,
            "sale_price": 0,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_sale_price_required_when_on_sale(self):
        data = {
            "name": "Laptop",
            "price": 800,
            "description": "On sale but no sale_price",
            "category": self.category.id,
            "is_sale": True,
            "sale_price": 0,  # Invalid
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_sale_price_optional_when_not_on_sale(self):
        data = {
            "name": "Laptop",
            "price": 800,
            "description": "Not on sale",
            "category": self.category.id,
            "is_sale": False,
            "sale_price": 0,
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
