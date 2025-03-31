from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterUserForm
import json
from cart.cart import Cart
from accounts.models import User
from store.models import Product


# dev_9
# Create your views here.
def logout_user(request):
    logout(request)
    return redirect("/")


# dev_9
def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # dev_23
            # 카트
            current_user = User.objects.get(id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                # Add
                cart = Cart(request)

                # {"1": {"quantity": 5, "price": "10000"}}
                # loop
                for product_id, data in converted_cart.items():
                    quantity = data["quantity"]
                    print("상품 ID:", product_id)  # 1
                    print("수량:", quantity)  # 5
                    product = Product.objects.get(id=product_id)
                    cart.add(product, quantity)

            messages.success(request, "You Have been logged in")
            return redirect("/")
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect("login")
    else:
        return render(request, "accounts/login.html", {})


# dev_11
def register_user(request):

    print("회원가입")

    if request.method == "POST":

        if request.POST["password1"] == request.POST["password2"]:

            form = RegisterUserForm(request.POST)

            if form.is_valid():
                form.save()  # DB 저장

                # 회원가입 하자 마자,  로그인을 시켜줌
                username = form.cleaned_data.get(
                    "username"
                )  # request.POST.get("username",'')
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(
                    username=username, password=raw_password
                )  # 사용자 인증
                login(request, user)  # 로그인

                return redirect("/")
    else:
        form = RegisterUserForm()

    return render(request, "accounts/register.html", {"form": form})
