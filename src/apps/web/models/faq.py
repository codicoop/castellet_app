from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock
from wagtail.fields import StreamField

from apps.web.models.base import BasePage, MenuLabelMixin


class QuestionAnswerBlock(StructBlock):
    question = CharBlock(
        required=True,
        label=_("Question"),
    )
    answer = RichTextBlock(
        required=True, label=_("Answer"), features=["bold", "italic", "link"]
    )

    class Meta:
        template = "web/components/faq_question_answer_block.html"
        icon = "circle-question"


class FaqPage(MenuLabelMixin, BasePage):
    questions = StreamField(
        [
            ("question", QuestionAnswerBlock()),
        ],
        null=False,
        blank=False,
        verbose_name=_("Questions & Answers"),
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("questions"),
    ]

    template = "web/pages/faq.html"
