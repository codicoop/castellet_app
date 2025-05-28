from constance import config
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.partners.choices import AccessPermissionRoleChoices
from apps.partners.models import Document, Project


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
        all_years = []
        for document in documents:
            all_tags.update((document.tags.all()))
            all_years.append(document.date_document.year)
        context = {
            "documents": documents,
            "projects": projects_with_documents,
            "tags": sorted(all_tags),
            # Convert to set to unify values, then to list again, and sort it
            "years": sorted(list(set(all_years))),
        }
        return render(request, "partners/documents.html", context)
    if request.htmx:
        selected_projects = request.POST.getlist("selected_projects")
        selected_tags = request.POST.getlist("selected_tags")
        selected_years = request.POST.getlist("selected_years")
        if (
            selected_projects == ["projects_all"]
            or selected_tags == ["tags_all"]
            or selected_years == ["years_all"]
        ):
            documents = Document.objects.filter(project__in=user_projects).distinct()
        if selected_projects and selected_projects != ["projects_all"]:
            documents = documents.filter(project__in=selected_projects)
        if selected_tags and selected_tags != ["tags_all"]:
            for tag in selected_tags:
                documents = documents.filter(tags=tag)
        if selected_years and selected_years != ["years_all"]:
            documents = documents.filter(date_document__year__in=selected_years)
        if not request.user.governing_council_member:
            documents = documents.filter(
                access_permission_role=AccessPermissionRoleChoices.ALL_USERS
            )
        context = {
            "projects": projects_with_documents,
            "documents": documents,
        }
        return render(request, "partners/documents_filtered.html", context)


@login_required
def project_list_view(request):
    context = {
        "projects": request.user.projects.all().order_by("title"),
        "contact_email": config.CONTACT_EMAIL,
        "contact_phone": config.CONTACT_PHONE,
    }
    return render(request, "partners/projects.html", context)


@login_required
def project_detail_view(request, id):
    project = get_object_or_404(Project, id=id, user_projects=request.user)
    context = {
        "project": project,
    }
    return render(request, "partners/project_details.html", context)
