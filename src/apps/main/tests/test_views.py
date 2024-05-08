from django.test import TestCase
from django.shortcuts import reverse

from django.test import Client


class NewsletterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse("newsletter"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/ca/newsletter/")

    def test_post(self):
        data = {
            "name": "test_name",
            "surnames": "test_surnames",
            "email": "test@test.com",
        }
        response = self.client.post(reverse("newsletter"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/ca/newsletter/success/")
