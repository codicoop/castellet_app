from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from apps.web.blocks import TitleTextBlock
from apps.web.models.base import BaseHeaderOverlayPage, MenuLabelMixin


class AboutUsPage(MenuLabelMixin, BaseHeaderOverlayPage):
    content = StreamField(
        [("title_text", TitleTextBlock()), ("horizontal_image", ImageChooserBlock())],
        null=False,
        blank=False,
    )

    content_panels = BaseHeaderOverlayPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "web/pages/about_us.html"
