from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from store.models import Product

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from accounts.models import User


# Create your views here.
# dev_15
class Cart(object):

    def __init__(self, request):
        self.session = request.session
        # dev_25
        # 로그인이 되어 있다면, 로그인 유저에 대한 정보를 빼내기 위하여...
        self.request = request

        print("유저========", self.request.user.username)

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    # {'quantity': 1, 'price': Decimal('10000.00'), 'product': <Product: 너를위한-장고>, 'total_price': Decimal('10000.00')}
    def __iter__(self):

        # {
        #     "1": {"quantity": 2, "price": "15000"},
        #     "3": {"quantity": 1, "price": "20000"}
        # }
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            # dev_24
            # dev_25 밑에서 is_sale 값을 price 에 넣고 있음
            # product = item["product"]

            # if product.is_sale:
            #     item["sale_price"] = product.sale_price
            #     item["sale_total_price"] = product.sale_price * item["quantity"]
            # else:
            #     item["sale_price"] = 0
            #     item["sale_total_price"] = 0

            yield item
        # https://chatgpt.com/c/67e8fc58-7a48-8007-8db2-1b97cb43ecb6
        # generator  처리후
        # {
        #     "quantity": 2,
        #     "price": Decimal("15000"),
        #     "total_price": Decimal("30000"),
        #     "product": Product(id=1, name="상품1")
        # }

    # ✅ 복호화된 세션 데이터: {'cart': {'1': {'quantity': 1, 'price': '24000.00'}}}
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            # dev_21
            if product.is_sale:
                self.cart[product_id] = {
                    "quantity": 0,
                    "price": str(product.sale_price),
                }
            else:
                self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if is_update:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

        # dev_23
        # if self.request.user.is_authenticated:
        #     current_user = User.objects.filter(id=self.request.user.id)
        #     # Convert {'3':1} to {"3":1}
        #     carty = str(self.cart)
        #     carty = carty.replace("'", '"')
        #     current_user.update(old_cart=str(carty))

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

        # dev_23
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            # Convert {'3':1} to {"3":1}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            current_user.update(old_cart=str(carty))

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    # dev_21
    def get_product_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    # dev_24
    def get_dic_cart(self):
        dic_cart = self.cart
        return dic_cart
