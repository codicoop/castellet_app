from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from apps.main.forms import NewsletterForm
from apps.main.services import send_confirmation_newsletter
from project.views import StandardSuccess


def newsletter_view(request):
    if request.method == "GET":
        form = NewsletterForm()
    else:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            send_confirmation_newsletter(form.data)
            return redirect("newsletter_success")
    return render(request, "newsletter.html", {"form": form})


class NewsletterSuccessView(StandardSuccess):
    page_title = _("Newsletter Successful")
    description = _("Newsletter created successful.")
