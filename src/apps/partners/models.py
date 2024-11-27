from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.partners.choices import (
    AccessPermissionRoleChoices,
    ProjectStatusChoices,
)
from project.models import BaseModel
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
        _("surnames"),
        max_length=100,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        null=False,
    )

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


class Project(BaseModel):
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
    description = models.TextField(
        _("Description"),
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

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"


class Document(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
        blank=False,
        default="",
    )
    description = models.CharField(
        _("Description"),
        max_length=500,
        blank=False,
        default="",
    )
    access_permission_role = models.CharField(
        _("Access Permission Role"),
        max_length=2,
        blank=False,
        choices=AccessPermissionRoleChoices.choices,
        default=AccessPermissionRoleChoices.ALL_USERS,
    )
    tags = TaggableManager(
        help_text=_("A comma-separated list of tags."),
        # Because Wagtail also has a Document model with tags in it
        # (AbstractDocument.tags) in which no related_name is specified, then
        # Django tries to create 2 reverse accessors with the same name
        # (Tag.document_set) and raises an error.
        related_name="partners_documents",
    )
    project = models.ManyToManyField(
        Project,
        blank=True,
        related_name="documents",
        verbose_name=_("Project"),
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
        related_name="documents",
    )
    date_document = models.DateField(
        _("Date of Document"),
        null=False,
        blank=False,
        default=timezone.now,
    )
    created_at = models.DateField(_("Upload date"), auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ["title"]

    def __str__(self):
        return self.title
