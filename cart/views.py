from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from store.models import Product
from cart.cart import Cart


# dev_15
# Create your views here.
def cart_add(request):

    cart = Cart(request)
    print("카트========", cart)

    if request.POST.get("action") == "post":

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


# dev_18
def cart_summary(request):
    # Get the cart
    cart = Cart(request)

    return render(
        request,
        "cart/cart_summary.html",
        {"cart": cart},
    )


# dev_19
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id =============== ", product_id)

        product = Product.objects.get(id=product_id)

        cart.remove(product)

        response = JsonResponse({"product": product_id})
        return response


# dev_20
def cart_update(request):
    cart = Cart(request)

    if request.POST.get("action") == "update":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id =============== ", product_id)

        quantity = int(request.POST.get("product_qty"))
        product = Product.objects.get(id=product_id)

        # def add(self, product, quantity=1, is_update=False):
        cart.add(product, quantity, True)

        response = JsonResponse({"product": product_id})
        return response
