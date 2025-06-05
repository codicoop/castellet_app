from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
)
from django.contrib.auth.forms import (
    PasswordChangeForm as BasePasswordChangeForm,
)
from django.contrib.auth.forms import (
    PasswordResetForm as BasePasswordResetForm,
)
from django.contrib.auth.forms import (
    SetPasswordForm as BaseSetPasswordForm,
)
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.partners.models import Project
from apps.users.models import User
from project.helpers import absolute_url
from project.post_office import send


class AuthenticationForm(BaseAuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(), label=_("Remember me")
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = _("Email or DNI")


class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
            }
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        password_reset_url = absolute_url(
            reverse(
                "registration:password_reset_confirm",
                kwargs={
                    "uidb64": context["uid"],
                    "token": context["token"],
                },
            )
        )
        context = {
            "project_name": config.PROJECT_NAME,
            "user_name": context["user"].full_name,
            "date": str(
                formats.date_format(
                    timezone.now().date(),
                    format="SHORT_DATE_FORMAT",
                    use_l10n=True,
                )
            ),
            "time": str(formats.time_format(timezone.localtime(timezone.now()).time())),
            "user_email": context["email"],
            "absolute_url": settings.ABSOLUTE_URL,
            "password_reset_url": password_reset_url,
        }
        send(
            recipients=[
                to_email,
            ],
            template="password_reset",
            context=context,
        )


class PasswordResetConfirmForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autofocus": True}),
        label=_("New password"),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("New password confirmation"),
    )


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
            }
        ),
        label=_("Old password"),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("New password"),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={}),
        label=_("New password confirmation"),
    )


class EmailVerificationCodeForm(forms.Form):
    email_verification_code = forms.CharField(
        widget=forms.TextInput(attrs=({"autofocus": True})),
        label=_("Verification code"),
    )


class SendVerificationCodeForm(forms.Form):
    pass


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    projects = forms.ModelMultipleChoiceField(
        label=_("Projects"),
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = []

    projects = forms.ModelMultipleChoiceField(
        label=_("Projects"),
        queryset=Project.objects.all().order_by("title"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
