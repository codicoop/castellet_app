from django import forms
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.main.models import Newsletter
from project.fields.flowbite import FormCharField, FormEmailField
from project.post_office import send


class NewsletterForm(forms.ModelForm):
    name = FormCharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": _("name"),
                "autocomplete": "text",
            }
        ),
        help_text="El teu nom",
    )
    surnames = FormCharField(
        widget=forms.TextInput(
            attrs={"placeholder": "cognoms", "autocomplete": "text"}
        ),
        help_text="Els teus cognoms",
    )
    email = FormEmailField(
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": _("email address")}
        ),
        help_text="Correu electrònic per subscriure't on rebràs el nostre butlletí",
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
