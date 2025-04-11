import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cart.cart import CartDRF
from orders.forms import ShippingForm
from orders.models import Order, OrderItem
from payment.models import Payment
from store.models import Product
from api.serializers import PaymentSerializer
from rest_framework import viewsets

# Create your views here.


# dev_39
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # create 커스텀 마이징
    def create(self, request, *args, **kwargs):

        cart = CartDRF(request)

        # 테스트용 결제 금액 검증 (실제에선 아임포트 서버 검증 필요)
        if 100 != int(request.data.get("paid_amount", 0)):
            return Response(
                {"error": "결제 금액이 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        # ✅ 1. 주문 생성
        order = Order.objects.create(user=user, amount_paid=cart.cart_total_price(user))

        # ✅ 2. 주문 아이템 추가
        # json.loads(old_cart)  # 딕셔너리 반환
        for product_id, item in json.loads(user.old_cart):
            OrderItem.objects.create(
                order=order,
                product_id=int(product_id),  # 외래키는 정수형 ID로 넘겨야 함
                quantity=item["quantity"],
                price=item["price"],
            )

        # ✅ 3. 배송지 정보 저장 (폼 방식 그대로 살릴 경우)
        form = ShippingForm(request.data)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = user
            shipping.order = order
            shipping.save()
        else:
            return Response({"error": "배송지 정보가 올바르지 않습니다."}, status=400)

        # ✅ 4. 결제 정보 저장
        payment = Payment.objects.create(
            order=order, imp_uid=request.data.get("imp_uid")
        )

        # ✅ 5. 장바구니 비우기
        user.old_cart = {}

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
