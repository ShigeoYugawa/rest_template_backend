# rest_template_backend/accounts/views.py

"""
accounts.views モジュール

ユーザー登録と認証機能

含まれる主なクラス:
- CustomerSignupView:  新規ユーザー登録 API ECなど一般ユーザー向け
- EmployeeSignupView:  新規ユーザー登録 API 基幹システムユーザー向け
- SNSSignupView:       新規ユーザー登録 API SNSなど一般ユーザー向け
- ActivateAccountView: 認証
- LoginView: ログイン
- LogoutView: ログアウト
"""

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import logout

from .serializers import (
    CustomerSignupSerializer,
    EmployeeSignupSerializer,
    SNSSignupSerializer,
)
from .models import CustomerProfile, EmployeeProfile, SNSProfile
from .email_service import send_activation_email

User = get_user_model()


class CustomerSignupView(generics.CreateAPIView):
    serializer_class = CustomerSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """.env.USE_EMAIL_VERIFICATIONを使用してメール認証を強制するか切替可能とする"""

        if getattr(settings, "USE_EMAIL_VERIFICATION", False):
            # メール認証フロー
            # ① 非アクティブで保存
            user = serializer.save(is_active=False)
            CustomerProfile.objects.create(user=user)

            # ② メール送信（サービス層へ委譲）
            send_activation_email(self.request, user)

        else:
            # 即ログインフロー
            user = serializer.save(is_active=True)
            CustomerProfile.objects.create(user=user)


class EmployeeSignupView(generics.CreateAPIView):
    serializer_class = EmployeeSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        サインアップ時の挙動を切り替える:
          - USE_EMAIL_VERIFICATION=True: メール認証フロー（is_active=False + 認証メール送信）
          - USE_EMAIL_VERIFICATION=False: 即ログインフロー（is_active=True）
        """
        if getattr(settings, "USE_EMAIL_VERIFICATION", False):
            # メール認証フロー
            user = serializer.save(is_active=False)
            EmployeeProfile.objects.create(
                user=user,
                department=serializer.validated_data.get("department", ""),
                position=serializer.validated_data.get("position", ""),
                hire_date=serializer.validated_data.get("hire_date"),
                qualifications=serializer.validated_data.get("qualifications", ""),
            )
            send_activation_email(user, self.request)
        else:
            # 即ログインフロー
            user = serializer.save(is_active=True)
            EmployeeProfile.objects.create(
                user=user,
                department=serializer.validated_data.get("department", ""),
                position=serializer.validated_data.get("position", ""),
                hire_date=serializer.validated_data.get("hire_date"),
                qualifications=serializer.validated_data.get("qualifications", ""),
            )


class SNSSignupView(generics.CreateAPIView):
    serializer_class = SNSSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        サインアップ時の挙動を切り替える:
          - USE_EMAIL_VERIFICATION=True: メール認証フロー（is_active=False + 認証メール送信）
          - USE_EMAIL_VERIFICATION=False: 即ログインフロー（is_active=True）
        """
        if getattr(settings, "USE_EMAIL_VERIFICATION", False):
            # メール認証フロー
            user = serializer.save(is_active=False)
            SNSProfile.objects.create(
                user=user,
                nickname=serializer.validated_data.get("nickname", ""),
                bio=serializer.validated_data.get("bio", ""),
            )
            send_activation_email(user, self.request)
        else:
            # 即ログインフロー
            user = serializer.save(is_active=True)
            SNSProfile.objects.create(
                user=user,
                nickname=serializer.validated_data.get("nickname", ""),
                bio=serializer.validated_data.get("bio", ""),
            )


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except Exception:
            return Response({"detail": "無効なリンクです。"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "アカウントが有効化されました。"}, status=200)
        else:
            return Response({"detail": "リンクが無効または期限切れです。"}, status=400)
        

class LoginView(ObtainAuthToken):
    """
    ユーザー名 / メールアドレス + パスワードで認証してトークンを返す
    """
    def post(self, request, *args, **kwargs):
        # ObtainAuthTokenの処理でuserを取得
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # トークンを取得または作成
        token = Token.objects.get_or_create(user=user)[0]

        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email,
        })
    

class LogoutView(APIView):
    """
    認証済みユーザーのトークンを削除してログアウト
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Tokenを削除
        logout(request)  # Sessionも削除（必要であれば）
        return Response({"detail": "ログアウトしました。"}, status=200)