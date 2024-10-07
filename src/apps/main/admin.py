import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.main.forms import DocumentAdminForm
from apps.main.models import Document, NewsletterSubscriber, Project, ProjectType
from apps.users.models import User


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
        "is_public",
    )
    list_filter = ("project_type", "status", "created_at", "is_public")
    search_fields = ["title", "created_at"]
    readonly_fields = [
        "documents_list",
        "participants_list",
        "number_participants",
    ]

    @admin.display(description=_("Documents"))
    def documents_list(self, *args):
        return ", ".join(
            [document.title for document in Document.objects.filter(project=args[0].id)]
        )

    @admin.display(description=_("Participants"))
    def participants_list(self, *args):
        return ", ".join(
            [
                participant.full_name
                for participant in User.objects.filter(projects=args[0].id)
            ]
        )

    @admin.display(description=_("Number of participants"))
    def number_participants(self, *args):
        return User.objects.filter(projects=args[0].id).count()


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = (
        "title",
        "get_projects",
        "get_tags",
        "access_permission_role",
        "responsible_user",
        "date_document",
    )
    list_filter = [
        "project",
        "access_permission_role",
        "responsible_user",
        "tags",
    ]
    search_fields = [
        "project",
        "title",
        "tags",
        "date_document",
        "file",
        "date_document",
        "access_permission_role",
    ]

    readonly_fields = [
        "created_at",
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

    def get_projects(self, obj):
        return ", ".join([project.title for project in obj.project.all()])

    get_projects.short_description = _("Projects")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    get_tags.short_description = _("Tag list")
