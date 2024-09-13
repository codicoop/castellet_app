from apps.web.models.base import BaseHeaderOverlayPage, MenuLabelMixin


class ProjectListPage(MenuLabelMixin, BaseHeaderOverlayPage):
    template = "web/pages/projects_list.html"
    parent_page_types = ["web.HomePage"]


class ProjectDetailPage(BaseHeaderOverlayPage):
    template = "web/pages/project_details.html"
    parent_page_types = ["web.ProjectListPage"]
    max_count = 1
    max_count_per_parent = 1
    show_in_menus_default = False
