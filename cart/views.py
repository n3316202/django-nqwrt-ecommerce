from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from cart.cart import Cart
from store.models import Product


# dev_15
# Create your views here.
def cart_add(request):

    cart = Cart(request)

    print("카트========", cart)

    if request.POST.get("action") == "post":
        print("=========")

        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id", product_id)

        product_qty = int(request.POST.get("product_qty"))
        # lookup proudct in DB
        product = get_object_or_404(Product, id=product_id)

        print("프로덕트", product)

        # save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({"qty": cart_quantity})

        return response

    print("카트========마지막")
