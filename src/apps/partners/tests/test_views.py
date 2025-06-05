from django.shortcuts import reverse
from django.test import Client, TestCase

from apps.users.models import User


class DocumentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            name="test_name",
            surnames="test_surnames",
            email="test@test.com",
            dni="12345678A",
            email_verified=True,
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse("partners:documents"))
        self.assertEqual(response.status_code, 200)
