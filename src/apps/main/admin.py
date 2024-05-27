import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.main.models import Newsletter, Project, Document


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export selected to CSV file")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("email", "name", "surnames", "created_at")
    search_fields = ["email", "name", "surnames", "created_at"]
    actions = ["export_as_csv"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ["name", "created_at"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "file", "created_at")
    search_fields = ["project", "title", "file", "created_at"]
