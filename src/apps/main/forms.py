from django import forms
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.main.choices import AccessPermissionRoleChoices
from apps.main.models import Document, NewsletterSubscriber, Project
from project.post_office import send


class NewsletterSubscriberForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "autocomplete": "text",
            }
        ),
    )
    surnames = forms.CharField(
        label=_("Surnames"),
        widget=forms.TextInput(attrs={"autocomplete": "text"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
        help_text=_("Email where you will receive our newsletter"),
    )

    class Meta:
        model = NewsletterSubscriber
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


class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "title",
            "description",
            "access_permission_role",
            "tags",
            "project",
            "file",
            "responsible_user",
            "date_document",
        ]

    access_permission_role = forms.ChoiceField(
        label=_("Access Permission Role"),
        choices=AccessPermissionRoleChoices.choices,
        widget=forms.RadioSelect,
    )

    project = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all().order_by("title"),
        widget=forms.CheckboxSelectMultiple,
        label=_("Projects"),
        required=False,
    )
