from django.test import TestCase

from apps.partners.forms import NewsletterSubscriberForm


class NewsletterSubscriberFormTest(TestCase):
    def setUp(self):
        self.form = NewsletterSubscriberForm(
            data={
                "name": "",
                "surnames": "",
                "email": "test",
            }
        )

    def test_form_errors(self):
        self.assertFalse(self.form.is_valid())

        with self.subTest("Required fields"):
            self.assertTrue("name" in self.form.errors)
            self.assertTrue("surnames" in self.form.errors)
        with self.subTest("Other validations"):
            self.assertTrue("email" in self.form.errors)
