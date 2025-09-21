from django.urls import path
from .views import (
    CustomerSignupView,
    EmployeeSignupView,
    SNSSignupView,
    ActivateAccountView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    # サインアップ (API)
    path("signup/customer/", CustomerSignupView.as_view(), name="signup_customer"),
    path("signup/employee/", EmployeeSignupView.as_view(), name="signup_employee"),
    path("signup/sns/", SNSSignupView.as_view(), name="signup_sns"),

    # メール認証 (API)
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),

    # ログイン / ログアウト (API)
    path("login/", LoginView.as_view(), name="login_api"),
    path("logout/", LogoutView.as_view(), name="logout_api"),
]