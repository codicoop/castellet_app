from django.test import TestCase

from apps.main.models import Newsletter
from apps.main.tests.factories import NewsletterFactory


class DataTest(TestCase):
    def setUp(self):
        self.full_data = NewsletterFactory(
            name="Andrew",
            surnames="Mc Callahan",
            email="andrew@mc.test",
        )
        self.empty_data = NewsletterFactory(
            name="",
            surnames="",
            email="",
        )

    def test_save(self):
        with self.subTest("Full_data"):
            self.assertIsInstance(self.full_data, Newsletter)
            self.assertEqual(self.full_data.name, "Andrew")
            self.assertEqual(self.full_data.surnames, "Mc Callahan")
            self.assertEqual(self.full_data.email, "andrew@mc.test")

        with self.subTest("Empty_data"):
            self.assertIsInstance(self.empty_data, Newsletter)
            self.assertEqual(self.empty_data.name, "")
            self.assertEqual(self.empty_data.surnames, "")
            self.assertEqual(self.empty_data.email, "")
