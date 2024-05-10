from django.urls import path

from apps.main.views import document_list_view

app_name = "documents"
urlpatterns = [
    # Documents
    path("documents/", document_list_view, name="documents"),
]
