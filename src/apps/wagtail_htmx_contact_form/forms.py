from django import forms
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.html import strip_tags

from .models import ContactSubmission


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]

    def send_submission_notification(self, to, subject, post_data):
        body = self.get_body(post_data)
        msg = EmailMultiAlternatives(
            self.get_formatted_subject(subject, post_data),
            strip_tags(body),
            settings.DEFAULT_FROM_EMAIL,  # From
            [
                to,
            ],  # To (iterable)
        )
        msg.attach_alternative(body, "text/html")
        msg.send()

    @staticmethod
    def get_formatted_subject(subject, post_data):
        date = timezone.now().strftime("%d.%m.%Y %H:%M")
        subject = f"[WEB] {post_data['name']} {subject} - {date}"
        return subject

    @staticmethod
    def get_body(post_data):
        body = f"""
        Nou e-mail de contacte rebut al formulari <br><br>
        Nom: {post_data['name']}<br>
        E-mail: {post_data['email']}<br>
        Assumpte: {post_data['subject']}<br>
        Missatge:<br>
        {post_data['message']}<br><br>
        """
        return body
