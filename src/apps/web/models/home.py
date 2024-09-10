from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField

from apps.web.models.base import BaseHeaderOverlayPage


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
        features=[
            "h2",
            "h3",
            "bold",
            "italic",
            "link",
            "ul",
        ],
    )
    video_youtube_url = models.CharField(
        _("YouTube URL"),
        max_length=240,
        default="",
        blank=True,
    )

    content_panels = BaseHeaderOverlayPage.content_panels + [
        MultiFieldPanel(
            children=[
                FieldPanel("video_title"),
                FieldPanel("video_description"),
                FieldPanel("video_youtube_url",),
            ],
            heading=_("Video"),
        ),
    ]

    template = "web/pages/home.html"
    parent_page_types = ["wagtailcore.Page"]

    def can_display_video_block(self):
        return (
            self.video_title
            and self.video_description
            and self.video_youtube_url
        )
