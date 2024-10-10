import uuid

from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.main.choices import AccessPermissionRoleChoices, ProjectStatusChoices
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
        null=False,
        unique=True,
    )

    class Meta:
        verbose_name = _("project type")
        verbose_name_plural = _("project types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        _("Title"),
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Project title"),
    )
    project_type = models.ForeignKey(
        ProjectType,
        blank=False,
        null=False,
        related_name="project",
        on_delete=models.CASCADE,
        verbose_name=_("Project type"),
        help_text=_("Project type"),
    )
    status = models.CharField(
        _("Status"),
        max_length=2,
        choices=ProjectStatusChoices.choices,
        blank=False,
        null=False,
    )
    description = models.CharField(
        _("Description"),
        max_length=500,
        blank=False,
        null=False,
    )
    image = models.ImageField(
        _("Image"),
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        validators=[validate_image_file_extension],
    )
    energy_power = models.PositiveIntegerField(
        _("Energy power"),
        blank=True,
        null=True,
        help_text=_("Project energy power (kW)"),
    )
    annual_energy = models.PositiveIntegerField(
        _("Annual energy"),
        blank=True,
        null=True,
        help_text=_("Project annual energy (kWh/year)"),
    )
    investment = models.PositiveIntegerField(
        _("Investment"),
        blank=True,
        null=True,
        default=0,
        help_text=_("Project investment (€)"),
    )
    is_public = models.BooleanField(
        _("Is public"),
        default=False,
        blank=True,
        null=True,
        help_text=_("Is this project public?"),
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

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
    tags = TaggableManager(help_text=_("A comma-separated list of tags."))
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
