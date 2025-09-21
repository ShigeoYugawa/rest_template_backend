# rest_template_backend/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseSignupSerializer(serializers.ModelSerializer):
    """
    ユーザー作成の共通処理をまとめたベースクラス。
    各用途別の SignupSerializer はこれを継承して拡張する。
    """

    # パスワードは書き込み専用にする（レスポンスでは返さない）
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # email + password を基本とする
        fields = ("email", "password")

    def create(self, validated_data):
        """
        UserManager の create_user() を使ってユーザーを作成する。
        （パスワードのハッシュ化も自動で処理される）
        """
        return User.objects.create_user(**validated_data)


class CustomerSignupSerializer(BaseSignupSerializer):
    """
    顧客用のサインアップシリアライザ。
    現時点では email と password 以外の項目は追加しない。
    """

    class Meta(BaseSignupSerializer.Meta):
        # email, password に加えて email を明示（重複だが将来の拡張を想定）
        fields = BaseSignupSerializer.Meta.fields + ("email",)


class EmployeeSignupSerializer(BaseSignupSerializer):
    """
    従業員用のサインアップシリアライザ。
    部署・役職・入社日・資格情報などを追加で受け付ける。
    """

    department = serializers.CharField(required=False, allow_blank=True)
    position = serializers.CharField(required=False, allow_blank=True)
    hire_date = serializers.DateField(required=False, allow_null=True)
    qualifications = serializers.CharField(required=False, allow_blank=True)

    class Meta(BaseSignupSerializer.Meta):
        # 共通(email, password) + 従業員固有フィールド
        fields = BaseSignupSerializer.Meta.fields + (
            "department",
            "position",
            "hire_date",
            "qualifications",
        )


class SNSSignupSerializer(BaseSignupSerializer):
    """
    SNSユーザー用のサインアップシリアライザ。
    ニックネームと自己紹介文を追加で受け付ける。
    """

    nickname = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta(BaseSignupSerializer.Meta):
        # 共通(email, password) + SNS固有フィールド
        fields = BaseSignupSerializer.Meta.fields + ("nickname", "bio")


