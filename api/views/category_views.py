from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import CategorySerializer
from store.models import Category
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.generics import GenericAPIView
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# # dev_31
# class CategoriesAPI(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class CategoryAPI(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(Category, id=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         category = get_object_or_404(Category, id=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         category = get_object_or_404(Category, id=pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # dev_33
# class CategoriesMixins(
#     ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView
# ):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request)

#     def post(self, request, *args, **kwargs):
#         return self.create(request)


# class CategoryMixins(
#     RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
# ):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# dev_34
# class CategoriesAPI(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class CategoryAPI(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# http://127.0.0.1:8000/api/categories/
class CategoriesAPI(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # POST 요청 커스터마이징
    def create(self, request, *args, **kwargs):
        name = request.data.get("name")

        # 같은 이름의 카테고리가 이미 존재할 경우 오류
        if Category.objects.filter(name=name).exists():
            raise ValidationError(
                {"message": "이미 같은 이름의 카테고리가 존재합니다."}
            )

        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "카테고리가 성공적으로 생성되었습니다.",
            "category": response.data,
        }
        return response


# generics.RetrieveUpdateDestroyAPIView : 조회/수정/삭제
# http://127.0.0.1:8000/api/category/4/
class CategoryAPI(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # 조회 시 로그 찍기
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"[조회] 카테고리 ID {instance.id} - {instance.name}")
        return super().retrieve(request, *args, **kwargs)

    # 수정 시 로깅 및 응답 커스터마이징
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"[수정] 카테고리 '{instance.name}' → '{request.data.get('name')}'")
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "카테고리가 수정되었습니다.",
            "category": response.data,
        }
        return response

    # HTTP DELETE 요청 →
    # → destroy() 실행 →
    # → perform_destroy(instance) 호출 →
    # → 객체 삭제

    # 삭제 전에 체크: 이름이 "고정"인 경우 삭제 금지
    def perform_destroy(self, instance):
        if instance.name == "고정":
            raise PermissionDenied("이 카테고리는 삭제할 수 없습니다.")
        print(f"[삭제] 카테고리 {instance.name} 삭제됨")
        instance.delete()

    # 삭제 응답 커스터마이징
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(
            {"message": "카테고리가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )


# dev_35
# List Route
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
