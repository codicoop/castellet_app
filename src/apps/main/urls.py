from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.main.views import document_list_view
from project.views import home_view

app_name = "main"
urlpatterns = [
    path("", home_view, name="home"),
    # Documents
    path(_("documents/"), document_list_view, name="documents"),
]
