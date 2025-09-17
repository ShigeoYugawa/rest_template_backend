# rest_template_backend/accounts/views.py

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    """新規ユーザー登録用の API View

    - メールアドレスとパスワードを受け取り、ユーザーを作成します。
    - 作成時に `is_active=False` として保存され、まだログインはできません。
    - 登録後、ユーザーに認証メールを送信し、認証リンクを踏むことで有効化されます。

    Attributes:
        serializer_class (Serializer): 利用するシリアライザ（SignupSerializer）
        permission_classes (list): 誰でもアクセス可能（AllowAny）
    """

    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """ユーザー作成時の追加処理

        - serializer.save() によりユーザーを作成
        - 現在のサイトドメインを取得し、ユーザーごとの認証リンクを生成
        - send_mail を使ってメール送信

        Args:
            serializer (SignupSerializer): バリデーション済みのシリアライザインスタンス
        """
        # DBにユーザーを保存（is_active=False）
        user = serializer.save()

        # 現在のサイト情報を取得（例: localhost:8000）
        current_site = get_current_site(self.request)

        # 認証用リンクを生成 (例: http://localhost:8000/accounts/activate/1/)
        link = f"http://{current_site.domain}{reverse('activate', args=[user.pk])}"

        # ユーザーにメール送信
        send_mail(
            subject="アカウント認証",
            message=f"以下のリンクをクリックして認証してください:\n{link}",
            from_email=None,  # settings.DEFAULT_FROM_EMAIL が使われる
            recipient_list=[user.email],
        )

