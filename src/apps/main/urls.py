from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.main.views import document_list_view

app_name = "documents"
urlpatterns = [
    # Documents
    path(_("documents/"), document_list_view, name="documents"),
]
