# rest_template_backend/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 追加のフィールドが必要な場合はここに定義
    # 例：
    # age = models.PositiveIntegerField(null=True, blank=True)
    pass
