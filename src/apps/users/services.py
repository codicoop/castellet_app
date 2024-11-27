import csv

from constance import config
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from apps.users.utils import email_verification_code_regeneration
from project.helpers import absolute_url
from project.post_office import send


def send_confirmation_mail(user_instance):
    email_verification_code = email_verification_code_regeneration(user_instance)
    email_verification_url = absolute_url(
        reverse(
            "registration:user_validation",
        )
    )
    context = {
        "project_name": config.PROJECT_NAME,
        "user_name": user_instance.name,
        "date": str(
            formats.date_format(
                timezone.now().date(),
                format="SHORT_DATE_FORMAT",
                use_l10n=True,
            )
        ),
        "time": str(formats.time_format(timezone.localtime(timezone.now()).time())),
        "user_email": user_instance.email,
        "user_code": email_verification_code,
        "absolute_url": settings.ABSOLUTE_URL,
        "email_verification_url": email_verification_url,
    }
    send(
        recipients=[
            user_instance.email,
        ],
        template="email_verification",
        context=context,
    )


class ExportUserCsvMixin:
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=usuaris.csv"
        writer = csv.writer(response)

        writer.writerow(
            [
                _("name"),
                _("surnames "),
                _("email address"),
                _("Contact telephone"),
                _("Address"),
                _("National Identity Document"),
                _("Bank account"),
                _("Charge"),
                _("Is governing council member"),
                _("Projects"),
                _("Partner ID"),
                _("Entry year"),
                _("Corporate contribution"),
                _("Voluntary contribution"),
            ]
        )

        for obj in queryset:
            user_projects = obj.projects.all()
            project_names = ", ".join([project.title for project in user_projects])
            corporate_contribution = getattr(obj, "corporate_contribution", "")
            voluntary_contribution = getattr(obj, "voluntary_contribution", "")
            writer.writerow(
                [
                    getattr(obj, "name", ""),
                    getattr(obj, "surnames", ""),
                    getattr(obj, "email", ""),
                    getattr(obj, "phone", ""),
                    getattr(obj, "address", ""),
                    getattr(obj, "dni", ""),
                    getattr(obj, "bank_account", ""),
                    getattr(obj, "charge", ""),
                    "Sí" if getattr(obj, "governing_council_member", "") else "No",
                    project_names,
                    getattr(obj, "partner_id", ""),
                    getattr(obj, "entry_year", ""),
                    corporate_contribution + " €" if corporate_contribution else "",
                    voluntary_contribution + " €" if voluntary_contribution else "",
                ]
            )
        return response

    export_as_csv.short_description = _("Export selected to CSV file")
