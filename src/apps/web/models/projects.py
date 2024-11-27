from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from apps.partners.choices import ProjectStatusChoices
from apps.web.models.base import BaseHeaderOverlayPage, BasePage, MenuLabelMixin


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
        context["active_projects"] = (
            ProjectDetailPage.objects.live()
            .filter(
                status=ProjectStatusChoices.ACTIVE,
            )
            .order_by("title")
        )
        context["study_phase_projects"] = (
            ProjectDetailPage.objects.live()
            .filter(
                status=ProjectStatusChoices.STUDY_PHASE,
            )
            .order_by("title")
        )
        context["other_projects"] = (
            ProjectDetailPage.objects.live()
            .filter(
                status=ProjectStatusChoices.OTHER,
            )
            .order_by("title")
        )
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
            "This image is intended to be decorative and creative to accompany "
            "the content. Depending on the resolution and device of the user, "
            "the size and proportion will vary, and therefore parts of the "
            "image will be cropped. The recommended proportion is 2x1, with a "
            "minimum size of 2,000x1,000px."
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
            (
                "text",
                RichTextBlock(
                    features=[
                        "h2",
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "image",
                    ],
                ),
            ),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
        verbose_name=_("Paragraphs and pictures"),
    )
    partners_project = models.ForeignKey(
        "partners.Project",
        verbose_name=_("Related project in the Partners app"),
        help_text=mark_safe(
            format_lazy(
                _(
                    "If set, some project details from the projects section in the "
                    "partners app will be included in the website. To create or "
                    'edit those projects, go to the <a href="{link}">'
                    "admin panel</a>."
                ),
                link=reverse_lazy("admin:partners_project_changelist"),
            )
        ),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="web_pages",
    )
    show_in_home = models.BooleanField(
        _("Show in the home page"),
        default=False,
        help_text=_(
            "If selected, this project will appear on the home page in the "
            "'What do we offer?' block."
        ),
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("status"),
        FieldPanel("description"),
        FieldPanel("partners_project"),
        FieldPanel("content"),
    ]
    settings_panels = BasePage.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_in_home"),
            ],
            heading=_("Configuration of projects in the home page"),
        ),
    ]

    template = "web/pages/project_details.html"
    parent_page_types = ["web.ProjectListPage"]
    show_in_menus_default = False
    max_count = None
