# rest_template_backend/accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """マネージャークラスで、CustomUserモデルのユーザー作成を管理します。
    create_user と create_superuser メソッドを提供し、ユーザー作成時の処理を統一します。
    """

    def create_user(self, email, password=None, **extra_fields):
        """通常のユーザーを作成します。

        Args:
            email (str): ユーザーのメールアドレス（必須）
            password (str, optional): ユーザーパスワード
            **extra_fields: その他のカスタムフィールド

        Returns:
            CustomUser: 作成されたユーザーインスタンス

        Raises:
            ValueError: email が指定されていない場合に発生
        """
        if not email:
            raise ValueError("メールアドレスは必須です")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # 初回はメール認証などでアクティブ化
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """管理者（スーパーユーザー）を作成します。

        Args:
            email (str): メールアドレス（必須）
            password (str, optional): パスワード
            **extra_fields: その他のカスタムフィールド

        Returns:
            CustomUser: 作成されたスーパーユーザーインスタンス
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True  # スーパーユーザーは即アクティブ
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル。

    メールアドレスをユーザー名として使用し、パスワード認証を行います。
    権限管理には PermissionsMixin を利用。
    
    Attributes:
        email (str): ユーザーのメールアドレス（ユニーク）
        is_active (bool): アカウントが有効かどうか
        is_staff (bool): 管理画面アクセス権限を持つか
        objects (CustomUserManager): このモデル用のマネージャー
        USERNAME_FIELD (str): 認証に使用するフィールド（email）
        REQUIRED_FIELDS (list): create_superuser で必須の追加フィールド
    """

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
