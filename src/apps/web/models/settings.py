from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting


@register_setting
class Strings(BaseSiteSetting):
    email = models.EmailField(
        blank=True,
        verbose_name=_("Contact e-mail"),
        default="",
    )
    address = models.TextField(
        verbose_name=_("Address"),
        blank=True,
        default="",
    )
    phone = models.CharField(
        verbose_name=_("Phone"),
        blank=True,
        default="",
        max_length=30,
    )
    footer_name = models.CharField(
        verbose_name=_("Footer name"),
        blank=True,
        help_text=_("Legal name and year"),
        default="© Nom entitat SCCL, 2024",
        max_length=60,
    )
    title_prefix = models.CharField(
        verbose_name=_("Title prefix"),
        blank=False,
        help_text=_("This will be prefixed to every page title. the title is "
                    "shown in the browser's tab."),
        default="Castellet Sostenible",
        max_length=60,
    )
    authorship = models.CharField(
        verbose_name=_("Authorship"),
        blank=True,
        default="Desenvolupat per Codi Cooperatiu · Dissenyat per Utopig Studio",
        max_length=150,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("address"),
                FieldPanel("phone"),
            ],
            heading=_("Contact Details"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_prefix"),
                FieldPanel("footer_name"),
            ],
            heading=_("Header and footer"),
        )
    ]

    class Meta:
        verbose_name = _("Website strings")


@register_setting
class AnalyticsSettings(BaseSiteSetting):
    embed = models.TextField(
        _("Embed code"),
        default="",
        blank=True,
    )

    panels = [
        FieldPanel("embed"),
    ]
