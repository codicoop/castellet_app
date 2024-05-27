from django import forms
from django.utils import formats, timezone

from apps.main.models import Newsletter
from project.fields.flowbite import FormCharField, FormEmailField
from project.post_office import send


class NewsletterForm(forms.ModelForm):
    name = FormCharField(
        label="Nom",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "autocomplete": "text",
            }
        ),
    )
    surnames = FormCharField(
        label="Cognoms",
        widget=forms.TextInput(
            attrs={"autocomplete": "text"}
        ),
    )
    email = FormEmailField(
        label="Correu electrònic",
        widget=forms.EmailInput(
            attrs={"autocomplete": "email"}
        ),
        help_text="Correu electrònic on vols rebre el nostre butlletí",
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
