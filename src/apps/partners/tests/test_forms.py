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
            self.assertEqual(self.form.errors["name"], ["Aquest camp és obligatori."])
            self.assertEqual(
                self.form.errors["surnames"], ["Aquest camp és obligatori."]
            )
        with self.subTest("Other validations"):
            self.assertEqual(
                self.form.errors["email"],
                ["Introdueix una adreça de correu electrònic vàlida"],
            )
