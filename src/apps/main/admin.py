
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.main.forms import DocumentAdminForm
from apps.main.models import Document, Project, ProjectType
from apps.main.services import ExportProjectCsvMixin
from apps.users.models import User


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
        "is_public",
        "number_participants"
    )
    list_filter = ("project_type", "status", "created_at", "is_public")
    search_fields = ["title", ]
    readonly_fields = [
        "documents_list",
        "participants_list",
        "number_participants",
    ]
    actions = ["export_as_csv"]

    @admin.display(description=_("Documents"))
    def documents_list(self, *args):
        documents = Document.objects.filter(project=args[0].id)
        if documents.exists():
            link = [
                    format_html(
                        '<a href="{}">{}</a>',
                        reverse('admin:main_document_change', args=[doc.id]),
                        doc.title
                    )
                    for doc in documents
                ]
            return format_html(", ".join(link))
        return "-"


    @admin.display(description=_("Participants"))
    def participants_list(self, obj):
        participants = User.objects.filter(projects=obj.id)
        if participants.exists():
            link = [
                format_html(
                     '<a href="{}">{}</a>',
                    reverse('admin:users_user_change', args=[participant.id]),
                    participant.full_name
                )
                for participant in participants
            ]
            return format_html(", ".join(link))
        return "-"

    @admin.display(description=_("Number of participants"))
    def number_participants(self, *args):
        if Project.objects.all():
            return User.objects.filter(projects=args[0].id).count()
        return "-"


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
        "project__title",
        "title",
        "tags__name",
        "file",
        "date_document",
        "access_permission_role",
    ]
    readonly_fields = [
        "created_at",
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

    def get_projects(self, obj):
        return ", ".join([project.title for project in obj.project.all()])

    get_projects.short_description = _("Projects")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    get_tags.short_description = _("Tag list")


