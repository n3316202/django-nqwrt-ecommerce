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
