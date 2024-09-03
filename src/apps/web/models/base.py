from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page, PageManager


class RequestedLocalePageManager(PageManager):
    def requested_locale(self, request):
        # current_locale is included in the request using a middleware
        return self.get_queryset().filter(locale=request.current_locale)


class BasePage(Page):
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
            "Aquesta imatge està pensada per ser decorativa i crear "
            "acompanyar el contingut. Segons la resolució i el dispositiu de "
            "l'usuari, la mida i proporció variarà, i per tant es retallaran "
            "parts de la imatge. La proporció recomanada és de 2x1, amb una "
            "mida mínima de 2.000x1.000px."
        ),
    )

    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
    ]
    max_count = 1
    show_in_menus_default = False
    parent_page_types = ["cms_site.HomePage"]
    is_submitable = False
    is_unpublishable = False
    # Removing this dropdown is also removing the "Delete" page option that it
    # contains. If you enable it, make sure that you actually pretend to give
    # the editor access to every action it provides!
    show_more_dropdown_in_list_actions = False
    objects = RequestedLocalePageManager()

    class Meta:
        abstract = True


class MenuLabelMixin(models.Model):
    """
    Mixin for BasePage.
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
