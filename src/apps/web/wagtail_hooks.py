import csv
from datetime import datetime

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.snippets.bulk_actions.snippet_bulk_action import SnippetBulkAction
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from apps.partners.models import NewsletterSubscriber


@hooks.register("construct_settings_menu")
def hide_user_and_group_settings(request, menu_items):
    """
    Hides Users and Groups from the settings menu in Wagtail.
    We need that to leave the users management to Django's admin and the public
    app.

    If in the future you need to manage groups or users in Wagtail, check if
    this issue is resolved:
    https://github.com/wagtail/wagtail/issues/7410#issuecomment-2468115196

    There are problems related to this app extending AbstractBaseUser instead of
    AbstractUser.
    Wagtail counts on the User model to inherit from AbstractUser and therefore
    include `first_name` and `last_name` fields, among some other.

    Unless they fixed that or some other simpler solution is found, you'll need
    to create a custom user form for wagtail:
    https://docs.wagtail.org/en/stable/advanced_topics/customisation/custom_user_models.html
    """
    menu_items[:] = [
        item for item in menu_items if item.name not in ("users", "groups")
    ]


class NewsletterSubscribersViewSet(SnippetViewSet):
    model = NewsletterSubscriber
    icon = "comment-add"
    copy_view_enabled = False
    inspect_view_enabled = True
    add_to_admin_menu = True
    menu_label = _("Newsletter subscribers")
    menu_order = 210  # 000 being 1st, 100 2nd, etc.)
    list_display = (
        "name",
        "surnames",
        "email",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "name",
        "email",
        "surnames",
    )


register_snippet(NewsletterSubscribersViewSet)


@hooks.register("register_bulk_action")
class ExportNewsletterSubscribersBulkAction(SnippetBulkAction):
    models = [NewsletterSubscriber]
    display_name = _("Export")
    aria_label = _("Export neslettert subscribers to a Mailchimp-compatible CSV.")
    action_type = "newsletter-subscribers-export"
    template_name = "web/cms/confirm_csv_export.html"

    @classmethod
    def execute_action(cls, objects, **kwargs):
        for obj in objects:
            print(obj)
        return len(objects), 0

    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        date = datetime.now().strftime("%Y-%m-%d")
        response["Content-Disposition"] = f"attachment; filename={date}-butlleti.csv"
        writer = csv.writer(response)
        objects, objects_without_access = self.get_actionable_objects()
        self.get_csv(objects, writer)
        return response
        # response = super().post(request, *args, **kwargs)
        # return response

    @staticmethod
    def get_csv(users_queryset, writer):
        writer.writerow(
            [
                "Email",
                "Nom",
                "Cognom",
            ]
        )
        for user in users_queryset:
            user_info = [
                user.email,
                user.name,
                user.surnames or "",
            ]
            writer.writerow(user_info)
