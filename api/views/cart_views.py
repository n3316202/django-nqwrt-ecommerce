from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from cart.cart import Cart
from api.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated


# ✅ 결과적으로 API endpoint 예시:
# HTTP       Method	        Endpoint	 기능
# GET	   /api/cart/	   장바구니       조회
# POST	   /api/cart/	   장바구니에    상품 추가
# PUT	   /api/cart/	   장바구니    상품 수량 변경
# DELETE   /api/cart/	   상품 제거 or 전체 비우기
# 🔁 DELETE에서 product_id를 넘기면 해당 상품만 제거, 안 넘기면 전체 비움 처리됩니다.


class CartAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        장바구니 목록 조회
        """
        cart = Cart(request)
        data = []

        for item in cart:
            serialized_item = {
                "product": ProductSerializer(item["product"]).data,
                "quantity": item["quantity"],
                "price": str(item["price"]),
                "total_price": str(item["total_price"]),
            }
            data.append(serialized_item)

        print("테스트")
        print(data)

        cart_total_items = len(cart)
        cart_total_price = cart.get_product_total()
        return Response(
            {
                "cart": data,
                "cart_total_items": cart_total_items,
                "cart_total_price": cart_total_price,
            }
        )

    def post(self, request):
        """
        장바구니에 상품 추가
        """
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        print("상품", product_id, "갯수", quantity)
        cart = Cart(request)

        try:
            product = Product.objects.get(id=product_id)
            cart.add(product, quantity=quantity)
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
        장바구니에서 상품 제거 또는 전체 삭제
        """
        product_id = request.data.get("product_id")

        cart = Cart(request)

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                cart.remove(product)
                return Response({"message": "상품이 장바구니에서 제거되었습니다."})
            except Product.DoesNotExist:
                return Response({"error": "상품이 존재하지 않습니다."}, status=404)
        else:
            cart.clear()
            return Response({"message": "장바구니가 비워졌습니다."})
