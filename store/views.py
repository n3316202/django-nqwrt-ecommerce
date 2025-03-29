from django.shortcuts import render
from django.http import HttpResponse

from store.models import Product
from store.models import Category, Product
from django.contrib import messages
from django.shortcuts import redirect, render


# Create your views here.
# dev_5
def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


# dev_8
def about(request):
    return render(request, "store/about.html", {})


# dev_13
def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "store/product.html", {"product": product})


# dev_14
def category(request, foo):
    # Replace Hyphens with Spaces

    foo = foo.replace("-", " ")
    print("foo:" + foo)

    # Grab the category from the url
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        print(category)

        products = Product.objects.filter(category=category)
        print(products)

        return render(
            request,
            "store/category.html",
            {
                "products": products,
                "category": category,
                "categories": Category.objects.all,
            },
        )

    except:
        messages.success(request, ("카테고리가 존재하지 않습니다."))
        return redirect("store:home")


# dev_14
def category_summary(request):
    categories = Category.objects.all()
    return render(request, "store/category_summary.html", {"categories": categories})
