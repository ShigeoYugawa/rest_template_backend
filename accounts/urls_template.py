# accounts/urls_template.py (テンプレート用)
from django.urls import path
from .views_template import LoginTemplateView, LogoutTemplateView

urlpatterns = [
    # ログイン画面（フォーム表示＋認証処理）
    path("login/", LoginTemplateView.as_view(), name="login"),

    # ログアウト（GETで実行 → loginへリダイレクト）
    path("logout/", LogoutTemplateView.as_view(), name="logout"),
]
