from django.contrib import admin
from accounts.models import User

# Register your models here.


# 기본적인 관리자 페이지에서 Question을 등록
admin.site.register(User)
