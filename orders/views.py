from django.shortcuts import redirect, render

from cart.cart import Cart
from django.contrib import messages
from .models import Order, OrderItem


# dev_24
# Create your views here.
def orders_create(request):

    if request.POST:

        cart = Cart(request)
        # cart_products = cart.get_products
        # quantiles = cart.get_quantities
        # cart_delete = cart.delete

        # totals = cart.cart_total()
        # print(totals)

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

            

            # Get product info
            for product in cart_products():
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantiles().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

            # Delete cart item(만약 카트도 지우고 싶다면)
            for key in list(quantiles().keys()):
                cart_delete(key)

            messages.success(request, "주문이 완료 되었습니다.")
            return redirect("/")
        else:
            messages.success(request, "You Must be logged In To order the products")
            return redirect("/login")

    else:
        messages.success(request, "Access denied")
        return redirect("/")
