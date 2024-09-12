from django.utils.translation import gettext_lazy as _
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.permission_policies import ModelPermissionPolicy
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import ContactSubmission


class ReadonlyPermissionPolicy(ModelPermissionPolicy):

    def user_has_permission(self, user, action):
        if action in ("change", "delete", "add"):
            return False
        return user.has_perm(self._get_permission_name(action))


class ContactSubmissionViewSet(SnippetViewSet):
    model = ContactSubmission
    icon = "mail"
    copy_view_enabled = False
    inspect_view_enabled = True
    add_to_admin_menu = True
    menu_label = _("Form submissions")
    menu_order = 200  # 000 being 1st, 100 2nd, etc.)
    list_display = (
        "created",
        "name",
        "email",
        "subject",
        "message",
        UpdatedAtColumn(),
    )
    list_filter = ("created",)
    search_fields = (
        "name",
        "email",
        "message",
    )

    @property
    def permission_policy(self):
        return ReadonlyPermissionPolicy(self.model)


register_snippet(ContactSubmissionViewSet)
