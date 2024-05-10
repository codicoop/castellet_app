from django.db import models

from project.fields import flowbite
from project.storage_backends import PrivateMediaStorage


class Newsletter(models.Model):
    email = flowbite.ModelEmailField(
        "correu electronic",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="Correu electrònic per subscriure't on rebràs el nostre butlletí",
    )
    name = flowbite.ModelCharField(
        "nom",
        max_length=50,
        blank=False,
        null=False,
        help_text="El teu nom",
    )
    surnames = flowbite.ModelCharField(
        "cognoms",
        max_length=100,
        blank=False,
        null=False,
        help_text="Els teus cognoms",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = "newsletter"
        verbose_name_plural = "newsletters"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email}"

    def full_name(self):
        return f"{self.name} {self.surnames}".strip()


class Project(models.Model):
    name = flowbite.ModelCharField(
        "nom",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="Nom del projecte",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = "projecte"
        verbose_name_plural = "projectes"
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
        "Títol",
        max_length=50,
        blank=False,
        null=False,
        help_text="Títol del document",
    )
    file = models.FileField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="file name",
        storage=PrivateMediaStorage(),
        help_text="Fitxer",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = "document"
        verbose_name_plural = "documents"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} | Project: {self.project}"
