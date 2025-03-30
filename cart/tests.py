from django.test import TestCase
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime


class SessionTest(TestCase):

    def test_all_sessions(self):
        """DB에 저장된 모든 세션을 조회하고 복호화하여 출력하는 테스트"""

        # 1️⃣ **모든 세션 키 가져오기**
        session_keys = Session.objects.values_list("session_key", flat=True)
        print(f"🔹 저장된 세션 키 목록 ({len(session_keys)}개): {list(session_keys)}\n")

        # 2️⃣ **세션 키가 없으면 종료**
        if not session_keys:
            print("❌ 저장된 세션이 없습니다.")
            return

        # 3️⃣ **각 세션 키에 대해 데이터 복호화 및 출력**
        for session_key in session_keys:
            try:
                # 세션 데이터를 가져와서 복호화
                session = Session.objects.get(session_key=session_key)
                session_data = SessionStore(session_key=session_key).load()

                print(f"✅ 세션 키: {session_key}")
                print(
                    f"   - 생성 시간: {session.expire_date.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                print(f"   - 복호화된 데이터: {session_data}\n")

            except Exception as e:
                print(f"⚠️ 세션 키 {session_key} 복호화 실패: {e}")

    def test_encode_session(self):
        import base64
        import json

        # DB에서 가져온 session_data (서명 포함)
        raw_session_data = "eyJjYXJ0Ijp7IjEiOnsicXVhbnRpdHkiOjEsInByaWNlIjoiMjQwMDAuMDAifX19:1tyjmA:tzt1C0yh9PPEgMvt93p4lKap_MGAAQvYNwYssETAcYo"

        # 서명 분리 (':'를 기준으로 앞부분만 추출)
        encoded_data = raw_session_data.split(":")[0]

        # Base64 디코딩 후 JSON 변환
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        session_dict = json.loads(decoded_data)

        # 출력
        print("✅ 복호화된 세션 데이터:", session_dict)

    # def test_session_crud(self):
    #     """세션 생성, 조회, 수정, 삭제 테스트"""

    #     # 1️⃣ **세션 생성 (Create)**
    #     session = SessionStore()
    #     session["cart"] = {"1": {"quantity": 2, "price": "25000.00"}}
    #     session.create()  # 세션 저장 (DB에 새로운 세션 생성)
    #     session_key = session.session_key  # 생성된 세션 키 가져오기
    #     print(f"✅ 생성된 세션 키: {session_key}")

    #     # 2️⃣ **세션 조회 (Read)**
    #     session_from_db = SessionStore(session_key=session_key)
    #     session_data = session_from_db.load()
    #     print(f"🔍 조회된 세션 데이터: {session_data}")

    #     # 3️⃣ **세션 수정 (Update)**
    #     session_from_db["cart"]["1"]["quantity"] = 3  # 수량 변경
    #     session_from_db.save()
    #     updated_session_data = SessionStore(session_key=session_key).load()
    #     print(f"✏️ 수정된 세션 데이터: {updated_session_data}")

    #     # 4️⃣ **세션 삭제 (Delete)**
    #     Session.objects.get(session_key=session_key).delete()
    #     try:
    #         deleted_session = SessionStore(session_key=session_key).load()
    #     except Exception as e:
    #         print(f"❌ 세션 삭제 확인: {e}")  # 세션이 삭제되었으면 오류 발생
