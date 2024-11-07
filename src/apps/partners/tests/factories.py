from factory.django import DjangoModelFactory

from apps.partners.models import NewsletterSubscriber


class NewsletterSubscriberFactory(DjangoModelFactory):
    class Meta:
        model = NewsletterSubscriber
