from django.shortcuts import redirect, render

from apps.main.forms import NewsletterForm
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
