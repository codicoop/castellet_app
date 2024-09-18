from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from apps.web.models.base import BasePage, MenuLabelMixin


class LegalPage(MenuLabelMixin, BasePage):
    text = RichTextField(
        _("Text"),
        features=[
            "h2",
            "h3",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
        ],
    )
    content_panels = BasePage.content_panels + [
        FieldPanel(
            "text",
        ),
    ]

    template = "web/pages/legal.html"
