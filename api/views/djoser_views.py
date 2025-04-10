from djoser.views import TokenCreateView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from djoser.conf import settings as djoser_settings
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        user = serializer.user

        # ✅ 세션 로그인
        login(self.request, user)

        # ✅ JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # ✅ 응답 포맷 (Djoser 기본 JWT와 동일)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_200_OK,
        )
