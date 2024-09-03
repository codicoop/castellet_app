from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from apps.web.models.base import BasePage


class HomePage(BasePage):
    description = RichTextField(
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

    content_panels = BasePage.content_panels + [
        FieldPanel("description"),
    ]

    template = "web/pages/home.html"
    parent_page_types = ["wagtailcore.Page"]
