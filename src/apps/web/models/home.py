from django.apps import apps
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

    template = "pages/home.html"
    parent_page_types = ["wagtailcore.Page"]

    @property
    def display_collection_1(self):
        return (
            self.collection_1_page
            and self.collection_1_image
            and self.collection_1_title
        )

    @property
    def display_collection_2(self):
        return (
            self.collection_2_page
            and self.collection_2_image
            and self.collection_2_title
        )

    @property
    def display_collection_3(self):
        return (
            self.collection_3_page
            and self.collection_3_image
            and self.collection_3_title
        )

    @property
    def display_collections_section(self):
        return (
            self.display_collection_1
            or self.display_collection_2
            or self.display_collection_3
        )

    @property
    def display_custom_projects_section(self):
        return (
            self.custom_projects_page
            and self.custom_projects_image
            and self.custom_projects_title
        )

    def can_display_header_highlight(self):
        return (
            self.display_header_highlight
            and self.overlay_image
            and self.overlay_body
            and self.overlay_title
        )

    def get_context(self, request, *args, **kwargs):
        ctxt = super().get_context(request, *args, **kwargs)
        ctxt = self.add_news_to_context(ctxt)
        ctxt = self.add_posts_to_context(ctxt)
        return ctxt

    def add_news_to_context(self, context):
        news_model = apps.get_model("cms_site", "NewsPage")
        news_page = news_model.objects.first()
        if news_page:
            context.update(
                {
                    "news_url": news_page.localized.get_url(),
                }
            )
            return context
        return context

    def add_posts_to_context(self, context):
        instagram_post_model = apps.get_model("cms_site", "InstagramPost")
        posts = instagram_post_model.objects.all()[:3]
        if posts:
            context.update(
                {
                    "instagram_posts": posts,
                },
            )
            return context
        return context
