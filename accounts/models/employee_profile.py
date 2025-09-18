from django.db import models
from django.conf import settings


class EmployeeProfile(models.Model):
    """
    従業員プロフィール
    勤怠管理や社内向けアプリで利用することを想定。
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    department = models.CharField("部署", max_length=100, blank=True, null=True)
    position = models.CharField("役職", max_length=100, blank=True, null=True)
    hire_date = models.DateField("入社日", blank=True, null=True)
    qualifications = models.TextField(
        "保有資格",
        blank=True,
        null=True,
        help_text="保有している資格をカンマ区切りなどで入力",
    )

    class Meta:
        verbose_name = "従業員プロフィール"
        verbose_name_plural = "従業員プロフィール"

    def __str__(self):
        return f"{self.user.get_display_name()}（{self.department or '部署未設定'}）"
