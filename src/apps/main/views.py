from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

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
