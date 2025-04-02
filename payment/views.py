from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required

from payment.models import Payment
from django.contrib import messages

# Create your views here.


# dev_25
# Create your views here.
@login_required
def payment_process(request):

    # 결제 성공 시 로직
    # 1.주문 정보 저장을 위해 ajax 요청
    # 2.서버에서 결재금액과 주문금액(세션에 저장되어있는)이 일치하는지 확인
    # 3.일치하면 주문 정보 및 결재정보 저장
    if request.POST:

        cart = Cart(request)

        # 카트 데이타 프레임 가져오기
        df_cart = cart.get_data_frame_products()

        # if total_price == int(request.POST['paid_amount']): #테스트를 위하여 10으로 넣고 대입
        if 100 == int(request.POST["paid_amount"]):
            # logged in
            user = request.user

            # create order
            create_order = Order(user=user)
            create_order.amount_paid = df_cart["sum_price"].sum()
            create_order.save()

            # Add Order Items
            # Get the oorder ID
            order_id = create_order.pk

            for index, row in df_cart.iterrows():
                # Create Order Item
                create_order_item = OrderItem(
                    order_id=order_id,
                    product_id=row["id"],
                    quantity=row["quantity"],
                    price=row["final_price"],
                )
                create_order_item.save()

            # 결재 데이터 저장
            create_payment = Payment(order=create_order)
            create_payment.imp_uid = request.POST["imp_uid"]
            create_payment.save()

            # 카트를 담고 있는 세션 지우기
            # Delete cart item(만약 카트도 지우고 싶다면)
            for key in list(cart.cart.keys()):
                cart.delete(key)

            messages.success(request, "결재가 완료 되었습니다.")
            return HttpResponse("SUCCESS")
        else:
            messages.success(request, "결재 금액이 맞지않아 취소 되었습니다.")
            return redirect("/")
