from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.fields import RichTextField

from apps.partners.choices import ProjectStatusChoices
from apps.partners.models import Project
from apps.web.models.base import BaseHeaderOverlayPage, MenuLabelMixin


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
        context["active_projects"] = Project.objects.filter(
            status=ProjectStatusChoices.ACTIVE,
        ).order_by("title")
        context["study_phase_projects"] = Project.objects.filter(
            status=ProjectStatusChoices.STUDY_PHASE,
        ).order_by("title")
        context["other_projects"] = Project.objects.filter(
            status=ProjectStatusChoices.OTHER,
        ).order_by("title")
        return context


class ProjectDetailPage(BaseHeaderOverlayPage):
    template = "web/pages/project_details.html"
    parent_page_types = ["web.ProjectListPage"]
    max_count = 1
    max_count_per_parent = 1
    show_in_menus_default = False
