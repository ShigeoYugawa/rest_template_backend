# rest_template_backend/accounts/models/sns_profile.py

from django.db import models
from django.conf import settings


class SNSProfile(models.Model):
    """
    SNS向けプロフィール
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sns_profile",
    )
    nickname = models.CharField("ニックネーム", max_length=50, blank=True, null=True)
    bio = models.TextField("自己紹介", blank=True, null=True)
    avatar = models.ImageField("アバター画像", upload_to="avatars/", blank=True, null=True)


    class Meta:
        verbose_name = "SNSプロフィール"
        verbose_name_plural = "SNSプロフィール"


    def __str__(self):
        return self.nickname or self.user.get_display_name()
