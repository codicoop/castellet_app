from wagtail.blocks import CharBlock, RichTextBlock, StructBlock


class TitleTextBlock(StructBlock):
    title = CharBlock(
        max_length=80,
        required=True,
    )
    body = RichTextBlock(
        required=True,
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
    )

    class Meta:
        template = "web/components/about_us_title_text_block.html"
