from django.shortcuts import redirect, render

from cart.cart import Cart
from django.contrib import messages
from .models import Order, OrderItem
from store.models import Product

from orders.forms import ShippingForm
from orders.models import Order, OrderItem, ShippingAddress

from django.contrib.auth.decorators import login_required


# dev_24
# Create your views here.
# dev_25
@login_required(login_url="accounts:login_user")
def orders_create(request):

    if request.POST:
        cart = Cart(request)
        # Gether Order Info
        if request.user.is_authenticated:
            # logged in
            user = request.user

            # Create Order
            create_order = Order(user=user)
            create_order.amount_paid = cart.get_product_total()  # 총액
            create_order.save()

            # dev_24
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

            cart_keys = list(cart.get_dic_cart().keys())

            # Delete cart item(만약 카트도 지우고 싶다면)
            for product_id in cart_keys:
                product = Product.objects.get(id=product_id)
                cart.remove(product)

            # dev_25
            form = ShippingForm(request.POST)

            if form.is_valid():
                shipping = form.save(commit=False)  # 저장은 하지 않고 객체만 생성
                shipping.user = (
                    request.user
                )  # ForeignKey 값 추가 (현재 로그인한 사용자)
                shipping.save()  # 최종적으로 저장

            messages.success(request, "주문이 완료 되었습니다.")
            return redirect("/")  # 주문이 완료 되었으니 결제 모듈로 리다이렉트 시킴
        else:
            messages.success(request, "You Must be logged In To order the products")
            return redirect("/login")

    else:
        # Get Current uer's shipping Info
        # shipping_user = ShippingAddress.objects.get(id=request.user.id)
        # Get User's Shipping Form
        # form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, "orders/create.html")
