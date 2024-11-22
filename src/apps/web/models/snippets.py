from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext_lazy as _


@register_snippet
class FooterLogo(models.Model):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Logo"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=False,
    )
    pangels = [
        FieldPanel("logo"),
    ]

    def __str__(self):
        if self.logo:
            return self.logo.title
        return _("Footer logo without image")
