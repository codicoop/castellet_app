from django import forms
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.partners.choices import AccessPermissionRoleChoices
from apps.partners.models import Document, NewsletterSubscriber, Project
from project.post_office import send


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = [
            "name",
            "surnames",
            "email",
        ]
        help_texts = {
            "email": "",
        }

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Focus on form field whenever error occurred
        error_list = list(self.errors)
        for item in error_list:
            self.fields[item].widget.attrs.update({"autofocus": True})
            break


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
