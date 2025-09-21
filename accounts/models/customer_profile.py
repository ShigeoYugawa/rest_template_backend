# rest_template_backend/accounts/models/customer_profile.py

from django.db import models
from django.conf import settings


class CustomerProfile(models.Model):
    """
    ECサイトや顧客管理向けのプロフィール
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    firstname = models.CharField("名", max_length=50)
    lastname = models.CharField("姓", max_length=50)
    postcode = models.CharField("郵便番号", max_length=20, blank=True, null=True)
    address = models.TextField("住所", blank=True, null=True)
    phone_number = models.CharField("電話番号", max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = "顧客プロフィール"
        verbose_name_plural = "顧客プロフィール"


    def __str__(self):
        return f"{self.user.get_display_name()}（顧客）"
