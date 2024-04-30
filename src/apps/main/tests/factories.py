from factory.django import DjangoModelFactory

from apps.main.models import Newsletter


class NewsletterFactory(DjangoModelFactory):
    class Meta:
        model = Newsletter
