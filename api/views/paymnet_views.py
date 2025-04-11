from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
        imp_uid = request.data.get("imp_uid")
        order_id = request.data.get("order")

        if not imp_uid or not order_id:
            return Response(
                {"error": "imp_uid와 order 필드는 필수입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. 중복 결제 방지
        if Payment.objects.filter(imp_uid=imp_uid).exists():
            return Response(
                {"error": "이미 처리된 결제입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "해당 주문이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 2. 결제 저장
        payment = Payment.objects.create(
            order=order,
            imp_uid=imp_uid,
        )

        # 3. 주문 상태 업데이트 (선택 사항)
        order.status = "paid"  # 예: Order 모델에 'status' 필드가 있다면
        order.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
