from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from apps.web.models.base import BasePage, MenuLabelMixin


class HtmxContactPage(MenuLabelMixin, BasePage):
    name_label = models.CharField(
        _("name"),
        max_length=250,
        help_text=_("Label for the Name field."),
        default=_("Your name"),
    )
    email_label = models.CharField(
        _("email"),
        max_length=250,
        help_text=_("Label for the e-mail field."),
        default=_("Your e-mail"),
    )
    phone_label = models.CharField(
        _("subject"),
        max_length=250,
        help_text=_("Label for the Phone field."),
        default=_("Phone"),
    )
    subject_label = models.CharField(
        _("subject"),
        max_length=250,
        help_text=_("Label for the Subject field."),
        default=_("Subject"),
    )
    message_label = models.CharField(
        _("message"),
        max_length=250,
        help_text=_("Label for the Message field."),
        default=_("Message"),
    )
    personal_data_auth_label = models.CharField(
        _("personal data authorization"),
        max_length=250,
        help_text=_("Label for the Personal data authorization field."),
        default=_("I authorize my personal data treatment"),
    )
    personal_data_auth_text = models.TextField(
        _("personal data authorization legal text"),
        help_text=_(
            "Legal text displayed alongside the personal data "
            "authorization checkbox."
        ),
        default="",
        blank=True,
    )

    # Form settings
    success_msg = models.CharField(
        _("success message"),
        default=_("Message sent, thanks for contacting us!"),
        max_length=250,
    )
    to_address = models.EmailField(
        _("to address"),
        blank=True,
        help_text=_(
            "E-mail to notify when a new submission is received. Leave"
            " it empty to disable the notifications."
        ),
        default="",
    )
    notification_subject = models.CharField(
        _("subject"),
        blank=True,
        max_length=250,
        help_text=_(
            "If empty, you will not get e-mail notifications for new "
            "form submissions."
        ),
        default="",
    )

    field_labels = [
        FieldPanel("name_label", classname="full"),
        FieldPanel("email_label", classname="full"),
        FieldPanel("phone_label", classname="full"),
        FieldPanel("subject_label", classname="full"),
        FieldPanel("message_label", classname="full"),
        FieldPanel("personal_data_auth_label", classname="full"),
        FieldPanel("personal_data_auth_text", classname="full"),
    ]
    form_settings = [
        FieldPanel("success_msg", classname="full"),
        FieldPanel("to_address", classname="full"),
        FieldPanel("notification_subject", classname="full"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            field_labels,
            heading=_("Field labels"),
        ),
        MultiFieldPanel(
            form_settings,
            heading=_("Form settings"),
        ),
    ]

    template = "web/pages/contact.html"

    def serve(self, request, *args, **kwargs):
        form_class = self.get_contact_form()
        form = form_class()
        if request.method == "POST" and request.htmx:
            form = form_class(request.POST)
            if form.is_valid():
                if self.to_address and self.notification_subject:
                    form.send_submission_notification(
                        self.to_address,
                        self.notification_subject,
                        request.POST,
                    )
                submissions_model = self.get_submissions_model()
                if submissions_model:
                    form.save()
                # Clearing form data
                form = form_class()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    self.success_msg,
                )

        context = {
            **self.get_context(request, *args, **kwargs),
            "form": form,
        }
        return render(
            request,
            template_name=self.get_template(request, *args, **kwargs),
            context=context,
        )

    def get_template(self, request, *args, **kwargs):
        if request.htmx:
            return "web/pages/contact_form.html"
        return super().get_template(request, *args, **kwargs)

    @staticmethod
    def get_contact_form():
        from .forms import ContactUsForm

        return ContactUsForm

    @staticmethod
    def get_submissions_model():
        return ContactSubmission


class ContactSubmission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        _("name"),
        max_length=120,
    )
    email = models.EmailField(
        _("e-mail"),
        max_length=255,
    )
    subject = models.CharField(
        _("subject"),
        max_length=240,
    )
    message = models.TextField(
        _("message"),
    )
    personal_data_auth = models.BooleanField(
        _("Treatment of personal data authorization"),
    )

    class Meta:
        verbose_name = _("contact form submission")
        verbose_name_plural = _("contact form submissions")

    def __str__(self):
        return f"{self.subject} ({self.email}) on {self.created}"
