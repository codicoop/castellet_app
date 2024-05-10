from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.users.views import (
    EmailVerificationCompleteView,
    EmailVerificationView,
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetInvalidLinkView,
    PasswordResetView,
    SendVerificationCodeView,
    details_view,
    privacy_policy_view,
    signup_view,
)
from project.views import StandardSuccess

app_name = "registration"
urlpatterns = [
    # Registration
    path("registre/", signup_view, name="signup"),
    path("inicio_sessió/", LoginView.as_view(), name="login"),
    path(
        "tancar_sessió/",
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy("home"),
        ),
        name="logout",
    ),
    path(
        "restabliment_contrasenya/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "restabliment_contrasenya/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "restabliment_contrasenya/invalid-link/",
        PasswordResetInvalidLinkView.as_view(),
        name="invalid_link",
    ),
    path(
        "restabliment_contrasenya/fet/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "restabliment_contrasenya/complet/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "canvi_contrasenya/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "canvi_contrasenya/fet/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Profile
    path(
        "perfil/modificat/",
        StandardSuccess.as_view(
            url=reverse_lazy("registration:profile_details"),
        ),
        name="profile_details_success",
    ),
    path(
        "perfil/detalls/",
        details_view,
        name="profile_details",
    ),
    path(
        "validació_usuari/",
        EmailVerificationView.as_view(),
        name="user_validation",
    ),
    path(
        "envio_codi_verificació/",
        SendVerificationCodeView.as_view(),
        name="send_verification_code",
    ),
    path(
        "verificació-email-complet/",
        EmailVerificationCompleteView.as_view(),
        name="email_verification_complete",
    ),
    path(
        "politica_privacitat/",
        privacy_policy_view,
        name="privacy_policy",
    ),
]
