from django.core.paginator import Paginator
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from apps.web.models.base import BasePage, MenuLabelMixin


class NewsListPage(MenuLabelMixin, BasePage):
    template = "web/pages/news_list.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["news_list"] = NewsDetailPage.objects.live().order_by("-date")

        # Prepare tags for rendering and filter by it
        tag = request.GET.get("tag")
        all_news_tag_slug = "Totes"
        if tag and tag != all_news_tag_slug:
            context["news_list"] = context["news_list"].filter(tags__name=tag)
        # each tag will be a dictionary. The key is the tag slug, and the value
        # is the "active" True or False, for the template to style it.
        context["tags"] = {all_news_tag_slug: tag == all_news_tag_slug}
        context["tags"].update(
            {
                tagged_news.tag.slug: tagged_news.tag.slug == tag
                for tagged_news in TaggedNews.objects.all()
            }
        )

        # Pagination
        news_per_page = 9
        paginator = Paginator(context["news_list"], news_per_page)
        page_number = request.GET.get("page")
        context["news_list"] = paginator.get_page(page_number)

        return context


class NewsTag(TagBase):
    subpage_types = ["web.NewsDetailPage"]

    class Meta:
        verbose_name = "news tag"
        verbose_name_plural = "news tags"


class TaggedNews(ItemBase):
    tag = models.ForeignKey(
        NewsTag, related_name="tagged_news", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to="web.NewsDetailPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class NewsDetailPage(BasePage):
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Header image"),
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=False,
        help_text=_(
            "This image is intended to be decorative and creative to accompany "
            "the content. Depending on the resolution and device of the user, "
            "the size and proportion will vary, and therefore parts of the "
            "image will be cropped. The recommended proportion is 2x1, with a "
            "minimum size of 2,000x1,000px."
        ),
    )
    date = models.DateField(
        verbose_name=_("Date"),
        blank=False,
    )
    tags = ClusterTaggableManager(through=TaggedNews, blank=True)
    content = StreamField(
        [
            ("text", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=False,
        blank=False,
        verbose_name=_("Paragraphs and pictures"),
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("date"),
        FieldPanel("tags"),
        FieldPanel("content"),
    ]

    template = "web/pages/news_details.html"
    parent_page_types = ["web.NewsListPage"]
    show_in_menus_default = False
    max_count = None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["related_news"] = self.tags.similar_objects()[:3]
        return context
