from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page, PageManager, Orderable


class RequestedLocalePageManager(PageManager):
    def requested_locale(self, request):
        # current_locale is included in the request using a middleware
        return self.get_queryset().filter(locale=request.current_locale)


class BasePage(Page):
    display_join_us_block = models.BooleanField(
        verbose_name=_("Display join us block"),
        help_text=_("Show the join us block at the botton of this page. To "
                    "modify its content, go to Settings - Website "
                    "customization."),
        default=True,
    )
    max_count = 1
    show_in_menus_default = False
    parent_page_types = ["web.HomePage"]
    objects = RequestedLocalePageManager()

    settings_panels = [
        MultiFieldPanel(
            [
                FieldPanel("display_join_us_block"),
            ],
            heading=_("Sections visibility configuration"),
        ),
    ] + Page.settings_panels

    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        ctxt = super().get_context(request, *args, **kwargs)
        legal_page = (
            apps.get_model("web", "LegalPage")
            .objects
            .first()
        )
        contact_page = (
            apps.get_model("wagtail_htmx_contact_form", "HtmxContactPage")
            .objects
            .first()
        )
        faq_page = (
            apps.get_model("web", "FaqPage")
            .objects
            .first()
        )
        ctxt.update(
            {
                "legal_page": legal_page,
                "contact_page": contact_page,
                "faq_page": faq_page,
            },
        )
        return ctxt


class MenuLabelMixin(BasePage):
    """
    Mixin for BasePage.

    When creating mixins for Wagtail pages, you need to extend a wagtail
    page class (like Page or BasePage) and set Meta.abstract = True.
    """

    menu_label = models.CharField(
        _("Menu title"),
        max_length=15,
        null=True,
        blank=True,
        help_text=_("If not set, the menu title will be the page title."),
    )

    promote_panels = BasePage.promote_panels + [
        FieldPanel("menu_label"),
    ]
    show_in_menus_default = True

    class Meta:
        abstract = True


class BaseHeaderOverlayPage(BasePage):
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Header image"),
        on_delete=models.SET_NULL,
        related_name="+",
        # Needs to be true for initial migrations to work, given that we're
        # programatically creating a HomePage instance.
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
    header_description = models.CharField(
        _("Header description"),
        max_length=250,
        default="",
        blank=True,
    )
    header_button_text = models.CharField(
        _("Header button title"),
        max_length=20,
        default="",
        blank=True,
    )
    header_button_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Header button linked page"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    overlay_title = models.CharField(
        _("Title"),
        max_length=80,
        default="",
        blank=True,
    )
    overlay_body = models.TextField(_("Text"), default="", blank=True)
    overlay_button_text = models.CharField(
        _("Button title"),
        max_length=20,
        default="",
        blank=True,
    )
    overlay_button_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Linked page"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    overlay_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    display_header_highlight = models.BooleanField(
        _("Display header highlighted overlay"),
        default=True,
        help_text="Per mostrar el missatge superposat a la capçalera cal marcar "
                  "aquesta opció i omplir les dades del bloc "
                  f"{_('Header overlay message')}."
    )

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            children=[
                FieldPanel("header_image"),
                FieldPanel("header_description"),
                FieldPanel("header_button_text",),
                FieldPanel("header_button_page",),
            ],
            heading=_("Header"),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("overlay_title"),
                FieldPanel("overlay_body"),
                FieldPanel(
                    "overlay_button_text",
                ),
                FieldPanel(
                    "overlay_button_page",
                ),
                FieldPanel(
                    "overlay_image",
                ),
                FieldPanel("display_header_highlight"),
            ],
            heading=_("Header overlay message"),
        ),
    ]

    class Meta:
        abstract = True

    def can_display_header_highlight(self):
        return (
            self.display_header_highlight
            and self.overlay_image
            and self.overlay_body
            and self.overlay_title
            and self.overlay_image
        )
