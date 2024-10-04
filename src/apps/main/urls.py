from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.main.views import document_list_view, project_detail_view, project_list_view

app_name = "documents"
urlpatterns = [
    # Documents
    path(_("documents/"), document_list_view, name="documents"),
    # Projects
    path(_("projects/"), project_list_view, name="projects"),
    path(_("projects/<int:id>"), project_detail_view, name="project_detail"),
]
