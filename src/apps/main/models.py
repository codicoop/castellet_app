from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.main.choices import (
    AccessPermissionRoleChoices,
    ProjectStatusChoices,
    TagsChoices,
)
from project.storage_backends import PrivateMediaStorage


class NewsletterSubscriber(models.Model):
    email = models.EmailField(
        _("email address"),
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Email where you will receive our newsletter"),
    )
    name = models.CharField(
        _("name"),
        max_length=50,
        blank=False,
        null=False,
    )
    surnames = models.CharField(
        _("surname"),
        max_length=100,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("newsletter subscriber")
        verbose_name_plural = _("newsletter subscribers")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email}"

    def full_name(self):
        return f"{self.name} {self.surnames}".strip()


class ProjectType(models.Model):
    name = models.CharField(
        _("project type name"),
        max_length=50,
        blank=False,
        default="",
        unique=True,
    )

    class Meta:
        verbose_name = _("project type")
        verbose_name_plural = _("project types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
        blank=False,
        default="",
        unique=True,
    )
    project_type = models.ForeignKey(
        ProjectType,
        blank=False,
        default="",
        related_name="project",
        on_delete=models.CASCADE,
        verbose_name=_("Project type"),
    )
    status = models.CharField(
        _("Status"),
        max_length=2,
        choices=ProjectStatusChoices.choices,
        blank=False,
        default="",
    )
    description = models.CharField(
        _("Description"),
        max_length=500,
        blank=False,
        default="",
    )
    image = models.ImageField(
        _("Image"),
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        validators=[validate_image_file_extension],
    )
    energy_power = models.CharField(
        _("Energy power"),
        blank=True,
        default="",
        help_text=_("Project energy power (kW)"),
    )
    annual_energy = models.CharField(
        _("Annual energy"),
        blank=True,
        default="",
        help_text=_("Project annual energy (kWh/year)"),
    )
    investment = models.CharField(
        _("Investment"),
        blank=True,
        default="",
        help_text=_("Project investment (€)"),
    )
    is_public = models.BooleanField(
        _("Is public"),
        blank=True,
        default=False,
        help_text=_("Is this project public?"),
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"


class Document(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Project"),
    )
    description = models.CharField(
        _("Description"),
        max_length=500,
        blank=False,
        null=False,
        help_text=_("Document description"),
    )
    access_permission_role = models.CharField(
        _("Access Permission Role"),
        max_length=2,
        blank=False,
        null=False,
        choices=AccessPermissionRoleChoices.choices,
        default=AccessPermissionRoleChoices.ALL_USERS,
        help_text=_("Access permission role"),
    )
    tags = models.CharField(
        _("Tags"),
        max_length=100,
        blank=False,
        null=False,
        choices=TagsChoices.choices,
    )
    project = models.ForeignKey(
        Project,
        null=False,
        blank=False,
        related_name="documents",
        verbose_name=_("Project"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        _("File"),
        max_length=100,
        blank=False,
        null=False,
        storage=PrivateMediaStorage(),
    )
    responsible_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Responsible user"),
    )
    date_document = models.DateField(
        _("Date of Document"),
        null=False,
        blank=False,
        default=timezone.now,
    )
    created_at = models.DateField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
