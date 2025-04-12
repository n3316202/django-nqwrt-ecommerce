from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from cart.cart import Cart, CartDRF
from api.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated


# ✅ 결과적으로 API endpoint 예시:
# HTTP       Method	        Endpoint	 기능
# GET	   /api/cart/	   장바구니       조회
# POST	   /api/cart/	   장바구니에    상품 추가
# PUT	   /api/cart/	   장바구니    상품 수량 변경
# DELETE   /api/cart/	   상품 제거 or 전체 비우기
# 🔁 DELETE에서 product_id를 넘기면 해당 상품만 제거, 안 넘기면 전체 비움 처리됩니다.

import json


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        장바구니 목록 조회
        """
        cart = json.loads(request.user.old_cart or "{}")

        cart_items = []
        total_quantity = 0
        total_price = Decimal("0.00")

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue  # 삭제된 상품은 제외

            price = product.sale_price if product.is_sale else product.price
            quantity = item.get("quantity", 0)
            item_total = Decimal(price) * quantity

            cart_items.append(
                {
                    "product": ProductSerializer(product).data,
                    "quantity": quantity,
                    "price": str(price),
                    "total_price": str(item_total),
                }
            )

            total_quantity += quantity
            total_price += item_total

        return Response(
            {
                "cart": cart_items,
                "cart_total_items": total_quantity,
                "cart_total_price": str(total_price),
            }
        )

    def post(self, request):
        """
        장바구니에 상품 추가
        """
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        print("상품", product_id, "갯수", quantity)
        cart = CartDRF(request)

        try:
            product = Product.objects.get(id=product_id)
            print("갯수5", quantity)
            price = product.sale_price if product.is_sale else product.price
            cart.add_to_old_cart(request.user, product.id, price, quantity)
            # cart.add(product, quantity=quantity)
            return Response({"message": "상품이 장바구니에 추가되었습니다."})
        except Product.DoesNotExist:
            return Response({"error": "상품이 존재하지 않습니다."}, status=404)

    def put(self, request):
        """
        장바구니 상품 수량 변경
        """
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        cart = Cart(request)

        try:
            product = Product.objects.get(id=product_id)
            cart.add(product, quantity=quantity, is_update=True)
            return Response({"message": "상품 수량이 변경되었습니다."})
        except Product.DoesNotExist:
            return Response({"error": "상품이 존재하지 않습니다."}, status=404)

    def delete(self, request):
        """
        old_cart에서 상품 제거 또는 전체 삭제
        """
        product_id = request.data.get("product_id")
        user = request.user
        cart = CartDRF(request)

        # 특정 상품 삭제
        if product_id:
            try:
                # 실제 존재하는 상품인지 확인
                product = Product.objects.get(id=product_id)
                cart.remove_from_old_cart(user, product_id)
                return Response({"message": "상품이 장바구니에서 제거되었습니다."})
            except Product.DoesNotExist:
                return Response({"error": "상품이 존재하지 않습니다."}, status=404)

        # 전체 비우기
        else:
            user.old_cart = "{}"
            user.save()
            return Response({"message": "장바구니가 비워졌습니다."})
