from django import forms
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.main.models import Newsletter
from project.fields.flowbite import FormCharField, FormEmailField
from project.post_office import send


class NewsletterForm(forms.ModelForm):
    name = FormCharField(
        label=_("Name"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": _("Name"),
                "autocomplete": "text",
            }
        ),
        help_text=_("Your name"),
    )
    surnames = FormCharField(
        label=_("Surnames"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Surnames"), "autocomplete": "text"}
        ),
        help_text=_("Your surnames"),
    )
    email = FormEmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": _("email address")}
        ),
        help_text=_("Email to subscribe where you will receive our newsletter"),
    )

    class Meta:
        model = Newsletter
        fields = [
            "name",
            "surnames",
            "email",
        ]

    def send_mail(self, context, to_email):
        context = {
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
        }
        send(
            recipients=[
                to_email,
            ],
            template="newsletter",
            context=context,
        )
