from factory.django import DjangoModelFactory

from apps.main.models import NewsletterSubscriber


class NewsletterSubscriberFactory(DjangoModelFactory):
    class Meta:
        model = NewsletterSubscriber
