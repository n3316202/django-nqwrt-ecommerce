from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from api.serializers.category_serializers import CategorySerializer
from store.models import Category

# http://127.0.0.1:8000/api/categories/
# 방식   url         기능
# GET   categories/    list


# dev_32
@api_view(["GET"])
def categories_api(request):

    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
