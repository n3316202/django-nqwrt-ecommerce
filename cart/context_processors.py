from .cart import Cart  # 현재폴더 cart.py 에서 Cart객체를 가져옴


# dev_17
def cart(request):
    print("컨텍스트 호출")
    return {"cart": Cart(request)}
