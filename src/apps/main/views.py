from django.shortcuts import redirect, render

from apps.main.forms import NewsletterForm
from apps.main.models import Document, Project
from apps.main.services import send_confirmation_newsletter


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
    if request.method == "GET":
        context = {
            "documents": Document.objects.all(),
            "projects": Project.objects.all(),
        }
        return render(request, "main/documents.html", context)
    if request.htmx:
        selected_projects = request.POST.getlist("selected_projects")
        context = {
            "documents": Document.objects.filter(project__in=selected_projects)
            if selected_projects
            else Document.objects.all(),
            "projects": Project.objects.all(),
        }
        return render(request, "main/documents_filtered.html", context)
