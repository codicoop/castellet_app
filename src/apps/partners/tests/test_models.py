from django.test import TestCase

from apps.partners.models import NewsletterSubscriber
from apps.partners.tests.factories import NewsletterSubscriberFactory


class NewsletterSubscriberTest(TestCase):
    def setUp(self):
        self.full_data = NewsletterSubscriberFactory(
            name="Andrew",
            surnames="Mc Callahan",
            email="andrew@mc.test",
        )
        self.empty_data = NewsletterSubscriberFactory(
            name="",
            surnames="",
            email="",
        )

    def test_save(self):
        with self.subTest("Full_data"):
            self.assertIsInstance(self.full_data, NewsletterSubscriber)
            self.assertEqual(self.full_data.name, "Andrew")
            self.assertEqual(self.full_data.surnames, "Mc Callahan")
            self.assertEqual(self.full_data.email, "andrew@mc.test")

        with self.subTest("Empty_data"):
            self.assertIsInstance(self.empty_data, NewsletterSubscriber)
            self.assertEqual(self.empty_data.name, "")
            self.assertEqual(self.empty_data.surnames, "")
            self.assertEqual(self.empty_data.email, "")
