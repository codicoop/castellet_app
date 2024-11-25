from wagtail import hooks


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
