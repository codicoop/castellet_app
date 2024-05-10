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
from django.utils.html import format_html

from apps.users.models import User
from project.fields import flowbite
from project.helpers import absolute_url
from project.post_office import send


class AuthenticationForm(BaseAuthenticationForm):
    username = flowbite.FormEmailField(
        label="Correu electrònic",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
                "placeholder": "Adreça de correu electronic",
            }
        ),
    )
    password = flowbite.FormPasswordField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contrasenya"}),
        label="Contrasenya",
    )
    remember_me = flowbite.FormBooleanField(
        required=False, widget=forms.CheckboxInput(), label="Recorda'm"
    )


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users with a different approach to password changing.
    """

    new_password = forms.CharField(
        label="Canvi de contrasenya",
        help_text="La contrasenya actual no es mostra per raons de seguretat. "
        "Utilitzeu aquest camp i deseu els canvis per establir una"
        " contrasenya nova. Mentre escrius la nova contrasenya serà"
        " visible per facilitar-te la còpia i l'enviament a l'usuari.",
        max_length=150,
        required=False,
    )

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_superuser")

    def save(self, commit=True):
        instance = super().save(commit)
        if self.cleaned_data.get("new_password", ""):
            instance.set_password(self.cleaned_data["new_password"])
        return instance


class UserSignUpForm(UserCreationForm):
    name = flowbite.FormCharField(
        label="Nom",
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Nom"}),
    )
    surnames = flowbite.FormCharField(
        label="Cognoms",
        widget=forms.TextInput(attrs={"placeholder": "Cognoms"}),
    )
    password1 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contrasenya"}),
        label="Contrasenya",
    )
    password2 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmació de contrasenya"}),
        label="Confirmació de contrasenya",
    )
    email = flowbite.FormEmailField(
        label="Correu electrònic",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Adreça de correu electrònic",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "name",
            "surnames",
            "password1",
            "password2",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        privacy_policy_url = self.get_privacy_policy_url()
        privacy_policy_link = '<a href="{}" class="text-primary-500 font-bold hover:underline" target="_blank">política de privacitat.</a>'.format(  # noqa: E501
            privacy_policy_url
        )
        label_html = "He llegit i estic d'acord amb {}".format(privacy_policy_link)
        self.fields["accept_conditions"] = flowbite.FormBooleanField(
            label=format_html(label_html), required=True
        )

    def get_privacy_policy_url(self):
        return reverse("registration:privacy_policy")

    def save(self, commit=True):
        obj = super().save(commit)
        obj.set_boolean_datetime(
            "privacy_policy_accepted", self.cleaned_data["accept_conditions"]
        )
        return obj


class ProfileDetailsForm(forms.ModelForm):
    name = flowbite.FormCharField(
        label="Nom",
        widget=forms.TextInput(attrs={"placeholder": "Nom"}),
    )
    surnames = flowbite.FormCharField(
        label="Cognoms",
        widget=forms.TextInput(attrs={"placeholder": "Cognoms"}),
    )
    email = flowbite.FormEmailField(
        label="Correu electrònic",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Adreça de correu electronic",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "name",
            "surnames",
            "email",
        )


class PasswordResetForm(BasePasswordResetForm):
    email = flowbite.FormEmailField(
        label="Correu electrònic",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
                "placeholder": "Adreça de correu electronic",
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
    new_password1 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(
            attrs={"autofocus": True, "placeholder": "Contrasenya nova"}
        ),
        label="Contrasenya nova",
    )
    new_password2 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmació de contrasenya nova"}
        ),
        label="Confirmació de contrasenya nova",
    )


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = flowbite.FormPasswordField(
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "placeholder": "Contrasenya antiga",
            }
        ),
        label="Contrasenya antiga",
    )
    new_password1 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contrasenya nova"}),
        label="Contrasenya nova",
    )
    new_password2 = flowbite.FormPasswordField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmació de contrasenya nova"}
        ),
        label="Confirmació de contrasenya nova",
    )


class EmailVerificationCodeForm(forms.Form):
    email_verification_code = flowbite.FormIntegerField(
        widget=forms.TextInput(
            attrs=({"autofocus": True, "placeholder": "Codi de verificació"})
        ),
        label="Codi de verificació",
    )


class SendVerificationCodeForm(forms.Form):
    pass
