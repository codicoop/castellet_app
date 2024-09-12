from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from apps.web.models.base import BaseHeaderOverlayPage


class TitleTextBlock(StructBlock):
    title = CharBlock(
        max_length=80,
        required=True,
    )
    body = RichTextBlock(
        required=True,
    )

    class Meta:
        template = "web/components/about_us_title_text_block.html"


class AboutUsPage(BaseHeaderOverlayPage):
    content = StreamField(
        [
            ("title_text", TitleTextBlock()),
            ("horizontal_image", ImageChooserBlock())
        ],
        null=False,
        blank=False,
    )

    content_panels = BaseHeaderOverlayPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "web/pages/about_us.html"
    parent_page_types = ["web.HomePage"]
