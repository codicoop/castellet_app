from django.shortcuts import reverse
from django.test import Client, TestCase

from apps.users.models import User


class NewsletterSubscriberViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse("newsletter"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/ca/butlleti/")
        self.assertTemplateUsed(response, "newsletter.html")

    def test_post(self):
        data = {
            "name": "test_name",
            "surnames": "test_surnames",
            "email": "test@test.com",
        }
        response = self.client.post(reverse("newsletter"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/ca/butlleti/alta/")
        self.assertTemplateUsed(response, "standard_success.html")


class DocumentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            name="test_name",
            surnames="test_surnames",
            email="test@test.com",
            dni="12345678A",
            email_verified=True
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse("main:documents"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/ca/documents/")
        self.assertTemplateUsed(response, "main/documents.html")
