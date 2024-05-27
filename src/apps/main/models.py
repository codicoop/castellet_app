from django.db import models
from django.utils.translation import gettext_lazy as _

from project.fields import flowbite
from project.storage_backends import PrivateMediaStorage


class Newsletter(models.Model):
    email = flowbite.ModelEmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Email to subscribe where you will receive our newsletter"),
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
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletters")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email}"

    def full_name(self):
        return f"{self.name} {self.surnames}".strip()


class Project(models.Model):
    name = flowbite.ModelCharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Project name"),
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"


class Document(models.Model):
    project = models.ForeignKey(
        Project,
        null=False,
        blank=False,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    title = flowbite.ModelCharField(
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Project"),
    )
    file = models.FileField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="file name",
        storage=PrivateMediaStorage(),
        help_text=_("File"),
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} | Project: {self.project}"
