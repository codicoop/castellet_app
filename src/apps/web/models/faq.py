from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, TextBlock
from wagtail.fields import StreamField

from apps.web.models.base import BasePage, MenuLabelMixin


class QuestionAnswerBlock(StructBlock):
    question = TextBlock(
        required=True,
        label=_("Question"),
    )
    answer = TextBlock(
        required=True,
        label=_("Answer"),
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
