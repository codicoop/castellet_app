from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
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


@login_required
def document_list_view(request):
    user_projects = request.user.projects.all()
    projects_with_documents = user_projects.filter(documents__isnull=False).distinct()
    documents = Document.objects.filter(project__in=user_projects).distinct()
    if not request.user.governing_council_member:
        documents = documents.filter(
            access_permission_role=AccessPermissionRoleChoices.ALL_USERS
        )
        projects_with_documents = projects_with_documents.filter(
            documents__access_permission_role=AccessPermissionRoleChoices.ALL_USERS
            )

    if request.method == "GET":
        all_tags = set()
        for document in documents:
            all_tags.update((document.tags.all()))
        context = {
            "documents": documents,
            "projects": projects_with_documents,
            "tags": sorted(all_tags),
        }
        return render(request, "main/documents.html", context)
    if request.htmx:
        selected_projects = request.POST.getlist("selected_projects")
        selected_tags = request.POST.getlist("selected_tags")
        if selected_projects == ["projects_all"]:
            documents = Document.objects.filter(project__in=user_projects).distinct()
        if selected_tags == ["tags_all"]:
            documents = Document.objects.filter(project__in=user_projects).distinct()
        if selected_projects and selected_projects != ["projects_all"]:
            documents = documents.filter(project__in=selected_projects)
        if selected_tags and selected_tags != ["tags_all"]:
            for tag in selected_tags:
                documents = documents.filter(tags=tag)
        if not request.user.governing_council_member:
            documents = documents.filter(
            access_permission_role=AccessPermissionRoleChoices.ALL_USERS
        )
        context = {
            "projects": projects_with_documents,
            "documents": documents,
        }
        return render(request, "main/documents_filtered.html", context)


@login_required
def project_list_view(request):
    context = {
        "projects": request.user.projects.all().order_by("title"),
    }
    return render(request, "main/projects.html", context)


@login_required
def project_detail_view(request, id):
    project = get_object_or_404(Project, id=id, user_projects=request.user)
    context = {
        "project": project,
    }
    return render(request, "main/project_details.html", context)
