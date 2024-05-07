from django.shortcuts import redirect, render

from apps.main.forms import NewsletterForm
from apps.main.models import Document, Project
from apps.main.services import send_confirmation_newsletter

from apps.main.constants import PROJECTS


def newsletter_view(request):
    if request.method == "GET":
        form = NewsletterForm()
    else:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            send_confirmation_newsletter(form.data)
            return redirect("home")
    return render(request, "newsletter.html", {"form": form})


def document_list_view(request):
    global PROJECTS
    if request.htmx:
        project_id = int(request.htmx.trigger)
        PROJECTS.append(project_id) if project_id not in PROJECTS else PROJECTS.remove(
            project_id
        )
        context = {
            "documents": Document.objects.filter(project__in=PROJECTS)
            if PROJECTS
            else Document.objects.all(),
            "projects": Project.objects.all(),
        }
        return render(request, "main/documents_filtered.html", context)
    if request.method == "GET":
        PROJECTS.clear()
        context = {
            "documents": Document.objects.all(),
            "projects": Project.objects.all(),
        }
        return render(request, "main/documents.html", context)
