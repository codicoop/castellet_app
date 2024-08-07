import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.main.models import Document, NewsletterSubscriber, Project, ProjectType


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


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("email", "name", "surnames", "created_at")
    search_fields = ["email", "name", "surnames", "created_at"]
    actions = ["export_as_csv"]


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_type",
        "status",
        "energy_power",
        "annual_energy",
        "investment",
        "created_at",
    )
    list_filter = ("project_type", "status", "created_at")
    search_fields = ["title", "created_at"]
    readonly_fields = [
        "participants",
        "number_participants",
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "tags", "file", "created_at")
    list_filter = [
        "project",
        "responsible_user",
        "tags",
    ]
    search_fields = ["project", "title", "tags", "date_document", "file", "created_at"]

    readonly_fields = [
        "responsible_user",
    ]

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.responsible_user:
            instance.responsible_user = user
        instance.save()
        form.save_m2m()
        return instance
