from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KakaoSocialAccountAdapter(DefaultSocialAccountAdapter):
    # 소셜 로그인 유저 객체를 초기화
    # User 모델 필드를 채워주는 메서드
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        kakao_data = sociallogin.account.extra_data
        kakao_account = kakao_data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})

        # 필수 필드
        user.email = kakao_account.get("email", "")
        user.profile_image = profile.get("profile_image_url")

        # gender 매핑 (카카오 → M/F)
        kakao_gender = kakao_account.get("gender")
        if kakao_gender == "male":
            user.gender = "M"
        elif kakao_gender == "female":
            user.gender = "F"

        # job 은 처음 가입 시 default 설정 (예: 기타)
        if not user.job:
            user.job = "E"

        return user

    # dev_41
    # DB에 저장되는 과정

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user (Kakao).
        """
        user = sociallogin.user

        print(user)
        # --- Kakao-specific data 처리 ---
        kakao_data = sociallogin.account.extra_data
        kakao_account = kakao_data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})

        # 이메일
        user.email = kakao_account.get("email", "")

        # 프로필 이미지
        user.profile_image = profile.get("profile_image_url")

        # 성별
        kakao_gender = kakao_account.get("gender")
        if kakao_gender == "male":
            user.gender = "M"
        elif kakao_gender == "female":
            user.gender = "F"

        # 직업 기본값 설정
        if not user.job:
            user.job = "E"  # 기타

        if not user.password:
            user.set_password(user.email)

        # if not user.username:
        #    user.username(user.email)

        # user.save()
        sociallogin.save(request)

        return user
