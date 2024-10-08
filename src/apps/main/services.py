import csv

from django.http import HttpResponse
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from project.post_office import send


def send_confirmation_newsletter(subscriber):
    context = {
        "user_name": subscriber["name"],
        "date": str(
            formats.date_format(
                timezone.now().date(),
                format="SHORT_DATE_FORMAT",
                use_l10n=True,
            )
        ),
        "time": str(formats.time_format(timezone.localtime(timezone.now()).time())),
        "user_email": subscriber["email"],
    }
    send(
        recipients=[
            subscriber["email"],
        ],
        template="newsletter",
        context=context,
    )


class ExportNewsletterCsvMixin:
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=newsletter.csv"
        writer = csv.writer(response)

        writer.writerow([
            _("email address"),
            _("name"),
        ])

        for obj in queryset:
            writer.writerow(
                [
                    getattr(obj, 'email', ''),
                    f"{getattr(obj, 'name', '')} {getattr(obj, 'surnames', '')}",
                ]
            )

        return response

    export_as_csv.short_description = _("Export selected to CSV file")

class ExportProjectCsvMixin:
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=projectes.csv"
        writer = csv.writer(response)

        writer.writerow([
            _("Title"),
            _("Project type"),
            _("Status"),
            _("Description"),
            _("Energy power"),
            _("Annual energy"),
            _("Investment"),
            _("Is public"),
            _("Participants"),
            _("Number of participants"),
        ])

        for obj in queryset:
            project_participants = obj.user_projects.all()
            participants = ", ".join([doc.name + " " + doc.surnames for doc in project_participants])
            writer.writerow(
                [
                    getattr(obj, 'title', ''),
                    getattr(obj, 'project_type', ''),
                    obj.get_status_display() if hasattr(obj, 'get_status_display') else '',
                    getattr(obj, 'description', ''),
                    getattr(obj, 'energy_power', '') + " kW" if getattr(obj, 'energy_power', '') else "",
                    getattr(obj, 'annual_energy', '') + " kWh/year" if getattr(obj, 'annual_energy', '') else "",
                    getattr(obj, 'investment', '') + " €" if getattr(obj, 'investment', '') else "",
                    "Sí" if getattr(obj, 'is_public', '') else "No",
                    participants,
                    project_participants.count()
                ]
            )

        return response

    export_as_csv.short_description = _("Export selected to CSV file")
