from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.main.choices import AccessPermissionRoleChoices
from apps.main.forms import NewsletterSubscriberForm
from apps.main.models import Document, Project
from apps.main.services import send_confirmation_newsletter
from project.views import StandardSuccess


def newsletter_view(request):
    if request.method == "GET":
        form = NewsletterSubscriberForm()
    else:
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            send_confirmation_newsletter(form.data)
            return redirect("newsletter_success")
    return render(request, "newsletter.html", {"form": form})


class NewsletterSubscriberSuccessView(StandardSuccess):
    page_title = _("Signed up to the newsletter")
    description = _("Successfully signed up to the newsletter.")


from icecream import ic


@login_required
def document_list_view(request):
    user_projects = request.user.projects.all()
    documents = Document.objects.filter(project__in=user_projects).distinct()
    if not request.user.governing_council_member:
        documents = documents.filter(
            access_permission_role=AccessPermissionRoleChoices.ALL_USERS
        )
    projects_with_documents = Project.objects.filter(
        documents__project__in=user_projects
    ).distinct()
    if request.method == "GET":
        all_tags = set()
        for document in documents:
            all_tags.update(document.tags.all())
        context = {
            "documents": documents,
            "projects": projects_with_documents,
            "tags": all_tags,
        }
        return render(request, "main/documents.html", context)
    if request.htmx:
        selected_projects = request.POST.getlist("selected_projects")
        selected_tags = ["2", "4"]
        ic(selected_tags)
        ic(selected_projects)
        if selected_projects:
            documents = documents.filter(project__in=selected_projects)
        if selected_tags:
            documents = documents.filter(tags__in=selected_tags)
            ic(documents)
        context = {
            "documents": documents,
        }
        return render(request, "main/documents_filtered.html", context)
