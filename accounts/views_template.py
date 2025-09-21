# rest_template_backend/accounts/views_template.py

"""
accounts.views_template モジュール

このモジュールは、Django標準のテンプレートレンダリング機能を利用して
ログイン／ログアウト機能を提供するクラスベースビューを定義しています。

主な特徴:
- REST API ではなく、HTML テンプレートを用いたフォームベース認証の実装
- Django の認証システム（authenticate, login, logout）を利用
- 成功・失敗時にメッセージフレームワークを使用してユーザーへ通知
- 成功時はリダイレクト、失敗時は同一テンプレートを再表示

含まれる主なクラス:
- LoginTemplateView: ログイン画面の表示とフォーム送信処理
- LogoutTemplateView: ログアウト処理を行いログイン画面へリダイレクト
"""


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

class LoginTemplateView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "ログインしました。")
            return redirect("home")  # 遷移先は適宜変更
        else:
            messages.error(request, "メールアドレスまたはパスワードが間違っています。")
            return render(request, self.template_name)


class LogoutTemplateView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "ログアウトしました。")
        return redirect("login")
