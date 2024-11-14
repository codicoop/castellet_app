from django.apps import apps
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from apps.partners.choices import ProjectStatusChoices
from apps.web.models.base import BaseHeaderOverlayPage, MenuLabelMixin, BasePage


class ProjectListPage(MenuLabelMixin, BaseHeaderOverlayPage):
    template = "web/pages/projects_list.html"
    parent_page_types = ["web.HomePage"]

    projects_active_title = models.CharField(
        _("Title"),
        max_length=200,
        default=_("Projects we are currently working on"),
        blank=False,
    )
    projects_active_description = RichTextField(
        _("Description"),
        features=["bold", "italic"],
        default="",
        blank=True,
    )
    projects_study_phase_title = models.CharField(
        _("Title"),
        max_length=200,
        default=_("Projects being studied"),
        blank=False,
    )
    projects_study_phase_description = RichTextField(
        _("Description"),
        features=["bold", "italic"],
        default="",
        blank=True,
    )
    projects_other_title = models.CharField(
        _("Title"),
        max_length=200,
        default=_("Future and other projects"),
        blank=False,
    )
    projects_other_description = RichTextField(
        _("Description"),
        features=["bold", "italic"],
        default="",
        blank=True,
    )

    content_panels = BaseHeaderOverlayPage.content_panels + [
        MultiFieldPanel(
            children=[
                FieldPanel("projects_active_title"),
                FieldPanel("projects_active_description"),
            ],
            heading=_("Currently active projects"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("projects_study_phase_title"),
                FieldPanel("projects_study_phase_description"),
            ],
            heading=_("Working on projects"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("projects_other_title"),
                FieldPanel("projects_other_description"),
            ],
            heading=_("Other and future projects"),
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["active_projects"] = ProjectDetailPage.objects.live().filter(
            status=ProjectStatusChoices.ACTIVE,
        ).order_by("title")
        context["study_phase_projects"] = ProjectDetailPage.objects.live().filter(
            status=ProjectStatusChoices.STUDY_PHASE,
        ).order_by("title")
        context["other_projects"] = ProjectDetailPage.objects.live().filter(
            status=ProjectStatusChoices.OTHER,
        ).order_by("title")
        return context


class ProjectDetailPage(BasePage):
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Header image"),
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=False,
        help_text=_(
            "Aquesta imatge està pensada per ser decorativa i crear "
            "acompanyar el contingut. Segons la resolució i el dispositiu de "
            "l'usuari, la mida i proporció variarà, i per tant es retallaran "
            "parts de la imatge. La proporció recomanada és de 2x1, amb una "
            "mida mínima de 2.000x1.000px."
        ),
    )
    status = models.CharField(
        _("Status"),
        max_length=2,
        choices=ProjectStatusChoices.choices,
        blank=False,
        default="",
    )
    description = RichTextField(
        verbose_name=_("Description"),
        features=["bold", "italic"],
        default="",
        blank=False,
    )
    content = StreamField(
        [
            ("text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
        verbose_name=_("Paragraphs and pictures"),
    )
    project = models.ForeignKey(
        "partners.Project",
        verbose_name=_("Related project in the Partners app"),
        help_text=mark_safe(
            format_lazy(
                _("If set, some project details from the projects section in the "
                  "partners app will be included in the website. To create or "
                  "edit those projects, go to the <a href=\"{link}\">"
                  "admin panel</a>."),
                link=reverse_lazy("admin:partners_project_changelist"),
            )
        ),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="web_pages",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("status"),
        FieldPanel("description"),
        FieldPanel("project"),
        FieldPanel("content"),
    ]

    template = "web/pages/project_details.html"
    parent_page_types = ["web.ProjectListPage"]
    show_in_menus_default = False
    max_count = None
