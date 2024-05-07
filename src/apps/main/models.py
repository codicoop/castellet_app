from django.db import models
from django.utils.translation import gettext_lazy as _

from project.fields import flowbite


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
        help_text=_("Your surnames)"),
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
