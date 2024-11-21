from wagtail.blocks import StructBlock, CharBlock, RichTextBlock


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
