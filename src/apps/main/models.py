from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from project.fields import flowbite
from project.storage_backends import PrivateMediaStorage


class NewsletterSubscriber(models.Model):
    email = flowbite.ModelEmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Email where you will receive our newsletter"),
    )
    name = flowbite.ModelCharField(
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Your name"),
    )
    surnames = flowbite.ModelCharField(
        max_length=100,
        blank=False,
        null=False,
        help_text=_("Your surnames"),
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
    name = flowbite.ModelCharField(
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
    class ProjectStatusChoices(models.TextChoices):
        PROJECT_STUDY_PHASE = "PS", _("Project in study phase")
        PROJECT_DEVELOPMENT = "AP", _("Active Project")
        OTHER_PROJECTS = "OP", _("Future projects or other projects")

    title = flowbite.ModelCharField(
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
    status = flowbite.ModelSelectDropdownField(
        _("Status"),
        max_length=2,
        choices=ProjectStatusChoices.choices,
        blank=False,
        null=False,
        help_text=_("Project status"),
    )
    description = flowbite.ModelCharField(
        _("Description"),
        max_length=500,
        blank=False,
        null=False,
        help_text=_("Project description"),
    )
    image = flowbite.ModelImageField(
        _("Image"),
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        validators=[validate_image_file_extension],
        help_text=_("Project image"),
    )
    energy_power = flowbite.ModelIntegerField(
        _("Energy power"),
        blank=True,
        null=True,
        help_text=_("Project energy power (kW)"),
    )
    annual_energy = flowbite.ModelIntegerField(
        _("Annual energy"),
        blank=True,
        null=True,
        help_text=_("Project annual energy (kWh/year)"),
    )
    investment = flowbite.ModelIntegerField(
        _("Investment"),
        blank=True,
        null=True,
        default=0,
        help_text=_("Project investment (€)"),
    )
    is_public = flowbite.ModelBooleanField(
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
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"

    @property
    def participants(self):
        from apps.users.models import User

        return ", ".join(
            [
                participant.full_name
                for participant in User.objects.filter(projects=self.id)
            ]
        )

    @property
    def number_participants(self):
        return len(self.participants.split(",")) if self.participants else 0


class Document(models.Model):
    class AccessPermissionRoleChoices(models.TextChoices):
        GOB_COUNCIL_DRIVING_GROUP = "GC", _("Governing Council and Driving Group")
        ALL_USERS = "AU", _("All users")

    class TagsChoices(models.TextChoices):
        GENERAL_ASSEMBLY = "GA", _("General Assembly")
        ACTS = "AC", _("Acts")
        BUDGETS_INVOICES = "BI", _("Budgets and invoices")
        CORPORATE = "CO", _("Corporate")

    title = flowbite.ModelCharField(
        _("Title"),
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Project"),
    )
    description = flowbite.ModelCharField(
        _("Description"),
        max_length=500,
        blank=False,
        null=False,
        help_text=_("Document description"),
    )
    access_permission_role = flowbite.ModelRadioField(
        _("Access Permission Role"),
        max_length=2,
        blank=False,
        null=False,
        choices=AccessPermissionRoleChoices.choices,
        default=AccessPermissionRoleChoices.ALL_USERS,
        help_text=_("Access permission role"),
    )
    tags = flowbite.ModelSelectCheckboxField(
        _("Tags"),
        max_length=100,
        blank=False,
        null=False,
        choices=TagsChoices.choices,
        help_text=_("Tags"),
    )
    project = models.ForeignKey(
        Project,
        null=False,
        blank=False,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    file = flowbite.ModelFileField(
        _("File"),
        max_length=100,
        blank=False,
        null=False,
        storage=PrivateMediaStorage(),
        help_text=_("File"),
    )
    responsible_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text=_("Responsible user"),
    )
    date_document = flowbite.ModelDateField(
        _("Date of Document"),
        null=False,
        blank=False,
        default=timezone.now(),
        help_text=_("Date of document"),
    )
    created_at = flowbite.ModelDateField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
