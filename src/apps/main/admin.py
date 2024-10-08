import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.main.models import Document, NewsletterSubscriber, Project, ProjectType
from apps.users.models import User
from apps.main.services import ExportNewsletterCsvMixin, ExportProjectCsvMixin


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin, ExportNewsletterCsvMixin):
    list_display = ("email", "name", "surnames", "created_at")
    search_fields = ["email", "name", "surnames", "created_at"]
    actions = ["export_as_csv"]


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin, ExportProjectCsvMixin):
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
        "documents_list",
        "participants_list",
        "number_participants",
    ]
    actions = ["export_as_csv"]

    @admin.display(description=_("Documents"))
    def documents_list(self, *args):
        return ", ".join(
            [document.title for document in Document.objects.filter(project=args[0].id)]
        )

    @admin.display(description=_("Participants"))
    def participants_list(self, *args):
        if Project.objects.all():
            return ", ".join(
                [
                    participant.full_name
                    for participant in User.objects.filter(projects=args[0].id)
                ]
            )
        return "-"

    @admin.display(description=_("Number of participants"))
    def number_participants(self, *args):
        if Project.objects.all():
            return User.objects.filter(projects=args[0].id).count()
        return "-"


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
    actions = ["export_as_csv"]

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.responsible_user:
            instance.responsible_user = user
        instance.save()
        form.save_m2m()
        return instance
