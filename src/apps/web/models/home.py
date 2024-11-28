from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, ChoiceBlock, StructBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField, StreamField

from apps.web.models.base import BaseHeaderOverlayPage
from apps.web.models.projects import ProjectDetailPage


class DocumentBlock(StructBlock):
    file = DocumentChooserBlock()

    class DocumentIconChoices(models.TextChoices):
        GENERAL = "doc-full-inverse", _("General document")
        IMAGE = "image", _("Image file")
        VIDEO = "desktop", _("Video file")
        AUDIO = "comment", _("Audio file")

    icon = ChoiceBlock(
        choices=DocumentIconChoices.choices,
        default=DocumentIconChoices.GENERAL,
    )
    title = CharBlock(
        max_length=80,
        required=True,
    )
    description = CharBlock(
        required=False,
    )


class HomePage(BaseHeaderOverlayPage):
    video_title = models.CharField(
        _("Title"),
        max_length=80,
        default="",
        blank=True,
    )
    video_description = RichTextField(
        _("Description"),
        default="",
        blank=True,
        features=[],
    )
    video_youtube_url = models.CharField(
        _("YouTube URL"),
        max_length=240,
        default="",
        blank=True,
    )
    documents_title = models.CharField(
        _("Title"),
        max_length=80,
        default="",
        blank=True,
    )
    documents_description = RichTextField(
        _("Description"),
        default="",
        blank=True,
        features=[],
    )
    documents = StreamField(
        [
            ("document", DocumentBlock()),
        ],
        null=True,
        blank=True,
    )
    projects_title = models.CharField(
        _("Title"),
        max_length=80,
        default=_("What does Castellet Sostenible offer?"),
        blank=False,
    )
    news_title = models.CharField(
        _("Title"),
        max_length=80,
        default=_("Last news"),
        blank=False,
    )

    content_panels = BaseHeaderOverlayPage.content_panels + [
        MultiFieldPanel(
            children=[
                FieldPanel("video_title"),
                FieldPanel("video_description"),
                FieldPanel("video_youtube_url"),
            ],
            heading=_("Video"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("documents_title"),
                FieldPanel("documents_description"),
                FieldPanel("documents"),
            ],
            heading=_("Documents"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("projects_title"),
                HelpPanel(
                    content=_(
                        "To add projects at the home page, you have to go navigate the "
                        "edit the project page (which are inside the Projects page in "
                        "the pages tree) and click the Configuration tab."
                    ),
                ),
            ],
            heading=_("Projects / What Castellet offers"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("news_title"),
                HelpPanel(
                    content=_(
                        "The latest news block is automatically generated taking the "
                        "latest 3 news created in the News page."
                    ),
                ),
            ],
            heading=_("Last news section"),
        ),
        MultiFieldPanel(
            children=[
                HelpPanel(
                    # Translators: Snippets in catalan is "Fragments"
                    content=_(
                        "To manage the logos for the 'With the support of...' footer "
                        "section, go to the Snippets section of the main menu."
                    ),
                ),
            ],
            heading=_("Footer logos"),
        ),
    ]

    template = "web/pages/home.html"
    parent_page_types = ["wagtailcore.Page"]

    def can_display_video_block(self):
        return self.video_title and self.video_description and self.video_youtube_url

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["last_news"] = apps.get_model(
            "web",
            "NewsDetailPage"
        ).objects.live().order_by("-date")[:3]
        context["news_page"] = apps.get_model("web", "NewsListPage").objects.first()
        context["projects"] = (
            ProjectDetailPage.objects.live()
            .filter(
                show_in_home=True,
            )
            .order_by("title")
        )
        return context
