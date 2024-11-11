from icecream import ic
from wagtail import hooks

@hooks.register("construct_settings_menu")
def hide_user_and_group_settings(request, menu_items):
    """
    Hides Users and Groups from the settings menu in Wagtail.
    We need that to leave the users management to Django's admin and the public
    app.

    If in the future you need to manage groups or users in Wagtail, you'll see that
    Wagtail by default expects the User model to inherit from BaseUser, which we do,
    but we removed some fields, i.ex. `last_name`.
    Wagtail will throw an error because of this.
    Therefore, you will need to create a custom user form for wagtail.
    Documentation: https://docs.wagtail.org/en/stable/advanced_topics/customisation/custom_user_models.html

    For the same reason, you'll se that when a user edits its own profile in Wagtail
    the Surnames field is empty, and
    """
    menu_items[:] = [item for item in menu_items if item.name not in ("users", "groups")]
