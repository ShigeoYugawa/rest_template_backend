# accounts/email_service.py

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activation_email(request, user):
    """
    ユーザーにアカウント有効化用メールを送信する。
    """

    # ① 認証URL生成
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    link = reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
    activate_url = f"http://{domain}{link}"

    # ② メール送信
    send_mail(
        "アカウント有効化",
        f"以下のリンクをクリックして有効化してください: {activate_url}",
        getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        [user.email],
    )
