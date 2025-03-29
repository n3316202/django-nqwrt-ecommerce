from django.contrib import admin
from accounts.models import User

# Register your models here.

# dev_12
# 1. 기본적인 관리자 페이지에서 기본적인 등록
# admin.site.register(User)


# 2.커스텀 모델을 등록하는 방법을 알았으니, 커스터마이징 옵션에 대해 알아보도록 하겠습니다.
class UserAccountsAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "job",
        "gender",
    ]

    # list_display = [
    #     "username",
    #     "email",
    #     "job",
    #     "gender",
    # ]

    # 커스터마이징 코드
    # 링크걸기
    list_display_links = [
        "username",
        "email",
        "job",
        "gender",
    ]

    list_filter = (
        "username",
        "email",
        "job",
        "gender",
    )

    search_fields = ["username", "email", "job"]


admin.site.register(User, UserAccountsAdmin)
