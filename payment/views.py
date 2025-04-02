from django.shortcuts import render

# Create your views here.
from sre_constants import POSSESSIVE_REPEAT
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from orders.models import Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required

from payment.models import Payment
from django.contrib import messages

from cart.cart import Cart
from django.contrib import messages
from store.models import Product

from orders.forms import ShippingForm
from orders.models import Order, OrderItem, ShippingAddress


# dev_26
# Create your views here.
@login_required(login_url="accounts:login_user")
def payment_process(request):

    # 결제 성공 시 로직
    # 1.주문 정보 저장을 위해 ajax 요청
    # 2.서버에서 결재금액과 주문금액(세션에 저장되어있는)이 일치하는지 확인
    # 3.일치하면 주문 정보 및 결재정보 저장
    if request.POST:

        cart = Cart(request)

        # if total_price == int(request.POST['paid_amount']): #테스트를 위하여 10으로 넣고 대입
        if 100 == int(request.POST["paid_amount"]):

            # logged in
            user = request.user

            # Create Order
            create_order = Order(user=user)
            create_order.amount_paid = cart.get_product_total()  # 총액
            create_order.save()

            # Add Order Items
            # Get the oorder ID
            order_id = create_order.pk

            # {'quantity': 1, 'price': Decimal('10000.00'), 'product': <Product: 너를위한-장고>, 'total_price': Decimal('10000.00')}
            for item in cart:
                print(item)
                # Create Order Item
                create_order_item = OrderItem(
                    order_id=order_id,
                    product_id=item["product"].id,
                    quantity=item["quantity"],
                    price=item["price"],
                )
                create_order_item.save()

            form = ShippingForm(request.POST)

            if form.is_valid():
                shipping = form.save(commit=False)  # 저장은 하지 않고 객체만 생성
                shipping.user = (
                    request.user
                )  # ForeignKey 값 추가 (현재 로그인한 사용자)
                shipping.save()  # 최종적으로 저장

            # 결재 데이터 저장
            create_payment = Payment(order=create_order)
            create_payment.imp_uid = request.POST["imp_uid"]
            create_payment.save()

            # Delete cart item(만약 카트도 지우고 싶다면)
            cart_keys = list(cart.get_dic_cart().keys())
            for product_id in cart_keys:
                product = Product.objects.get(id=product_id)
                cart.remove(product)

            messages.success(request, "결재가 완료 되었습니다.")
            return HttpResponse("SUCCESS")
        else:
            messages.success(request, "결재 금액이 맞지않아 취소 되었습니다.")
            return redirect("/")
