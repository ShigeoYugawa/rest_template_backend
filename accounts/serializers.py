# rest_template_backend/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """新規ユーザー登録用のシリアライザ

    - メールアドレスとパスワードを受け取り、ユーザーを作成します。
    - パスワードは write_only に設定されており、レスポンスには含まれません。

    Attributes:
        password (CharField): ユーザーのパスワード（書き込み専用）

    Meta:
        model (User): 使用するモデル（CustomUser）
        fields (tuple): シリアライズ対象のフィールド（email, password）
    """

    # レスポンスには含めず、書き込み専用にする
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        """バリデーション後のデータからユーザーを作成する。

        Args:
            validated_data (dict): バリデーション済みのデータ（email, password）

        Returns:
            User: 作成されたユーザーインスタンス
        """
        # CustomUserManager の create_user を呼び出す
        user = User.objects.create_user(**validated_data)
        return user

